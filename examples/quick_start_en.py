"""Docflow SDK quick start: expense reimbursement workflow (English).

Required sample files under examples/sample_files:

- 报销申请单.XLS (the filename is intentionally kept in Chinese)
- sample_hotel_receipt.png
- sample_payment_record.png
"""

import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from docflow import DocflowClient, ExtractModel, ReviewModel


def print_section(title):
    """Print a major section heading."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_step(number, description):
    """Print a workflow step heading."""
    print(f"\n[Step {number}] {description}")


def load_configuration():
    """Load a nearby .env file when present, then create the client."""
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).parent / ".env",
        Path(__file__).parent.parent / ".env",
    ]
    for env_path in candidates:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded configuration from {env_path}")
            break
    return DocflowClient.from_env()


def field_map(client, workspace_id, category_id):
    """Return a field-name-to-field-ID mapping for one category."""
    response = client.category.fields.list(
        workspace_id=workspace_id,
        category_id=category_id,
    )
    return {item.name: item.id for item in response.fields}, response.tables


def main():
    """Run the complete expense reimbursement quick start."""
    print_section("Docflow SDK Quick Start — Expense Reimbursement")
    client = load_configuration()
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_files")

    print_step(1, "Create a workspace")
    workspace = client.workspace.create(
        name=f"Expense_Reimbursement_{datetime.now():%Y%m%d_%H%M%S}",
        auth_scope=1,
        description="Automated expense reimbursement document processing",
    )
    workspace_id = workspace.workspace_id
    print(f"  Workspace created: {workspace_id}")

    print_step(2, "Configure document categories")
    print("  [2.1] Creating the reimbursement application category...")
    reimbursement = client.category.create(
        workspace_id=workspace_id,
        name="REIMBURSEMENT_APPLICATION",
        extract_model=ExtractModel.Acgpt,
        sample_files=[os.path.join(sample_dir, "报销申请单.XLS")],
        fields=[
            {"name": "Applicant"},
            {"name": "Trip Purpose"},
            {"name": "Reimbursement Period"},
            {"name": "Destination"},
            {"name": "Expense Date"},
            {"name": "Expense Item"},
            {"name": "Travel Expense Amount"},
            {"name": "Tax Rate"},
            {"name": "Loan Offset Amount"},
            {"name": "Requested Payment Amount"},
            {"name": "Notes"},
            {"name": "Tax Amount"},
        ],
        category_prompt=(
            "An expense reimbursement application containing applicant, "
            "business-trip, and expense details."
        ),
    )
    reimbursement_id = reimbursement.category_id
    reimbursement_fields, _ = field_map(client, workspace_id, reimbursement_id)
    print(f"    Category ID: {reimbursement_id}")

    print("  [2.2] Creating the hotel receipt category...")
    hotel = client.category.create(
        workspace_id=workspace_id,
        name="HOTEL_RECEIPT",
        extract_model=ExtractModel.Acgpt,
        sample_files=[os.path.join(sample_dir, "sample_hotel_receipt.png")],
        fields=[
            {"name": "Check-in Date"},
            {"name": "Check-out Date"},
            {"name": "Total Amount"},
        ],
        category_prompt="A hotel folio with dates, a total amount, and charge details.",
    )
    hotel_id = hotel.category_id
    hotel_table = client.category.tables.add(
        workspace_id=workspace_id,
        category_id=hotel_id,
        name="Charge Details",
        prompt="Extract the date, charge type, amount, and notes for each charge.",
    )
    for name in ["Date", "Charge Type", "Amount", "Notes"]:
        client.category.fields.add(
            workspace_id=workspace_id,
            category_id=hotel_id,
            table_id=hotel_table.table_id,
            name=name,
        )
    hotel_fields, hotel_tables = field_map(client, workspace_id, hotel_id)
    hotel_table_fields = {
        item.name: item.id
        for table in hotel_tables
        if table.name == "Charge Details"
        for item in table.fields
    }
    print(f"    Category ID: {hotel_id}")

    print("  [2.3] Creating the payment record category...")
    payment = client.category.create(
        workspace_id=workspace_id,
        name="PAYMENT_RECORD",
        extract_model=ExtractModel.Acgpt,
        sample_files=[os.path.join(sample_dir, "sample_payment_record.png")],
        fields=[
            {"name": "Transaction Number"},
            {"name": "Payee Name"},
            {"name": "Payer Name"},
            {"name": "Transaction Time"},
            {"name": "Transaction Amount"},
            {"name": "Currency"},
            {"name": "Payment Method"},
        ],
        category_prompt="An electronic payment record with parties and transaction details.",
    )
    payment_id = payment.category_id
    payment_fields, _ = field_map(client, workspace_id, payment_id)
    print(f"    Category ID: {payment_id}")

    print_step(3, "Upload documents")
    uploads = [
        ("报销申请单.XLS", "REIMBURSEMENT_APPLICATION"),
        ("sample_hotel_receipt.png", "HOTEL_RECEIPT"),
        ("sample_payment_record.png", "PAYMENT_RECORD"),
    ]
    task_ids = []
    for filename, category in uploads:
        response = client.file.upload(
            workspace_id=workspace_id,
            category=category,
            file_path=os.path.join(sample_dir, filename),
        )
        for item in response.files:
            if item.task_id:
                task_ids.append(item.task_id)
        print(f"  Uploaded {filename}; batch number: {response.batch_number}")

    print_step(4, "Wait for extraction results")
    extracted_files = []
    for elapsed in range(0, 120, 5):
        response = client.file.fetch(workspace_id=workspace_id, page_size=100)
        extracted_files = [item for item in response.files if item.task_id in task_ids]
        pending = [
            item for item in extracted_files
            if item.recognition_status in (0, 3, 4, 5)
        ]
        if not pending and len(extracted_files) == len(task_ids):
            print("  All documents have finished processing")
            break
        print(f"  {len(pending)} documents still processing ({elapsed}s elapsed)")
        time.sleep(5)

    for item in extracted_files:
        print(f"  {item.name}: status={item.recognition_status}")
        if item.data:
            print(f"    Extracted fields: {len(item.data.get('fields', []))}")

    print_step(5, "Configure review rules")
    repo = client.review.create_repo(
        workspace_id=workspace_id,
        name="Expense Reimbursement Review Rules",
    )
    repo_id = repo.repo_id

    completeness_group = client.review.create_group(
        workspace_id=workspace_id,
        repo_id=repo_id,
        name="Reimbursement Application Compliance",
    )
    client.review.create_rule(
        workspace_id=workspace_id,
        repo_id=int(repo_id),
        group_id=completeness_group.group_id,
        name="Required Field Completeness",
        prompt=(
            "Fail the review if Applicant, Expense Date, Expense Item, or "
            "Requested Payment Amount is empty."
        ),
        category_ids=[reimbursement_id],
        risk_level=10,
        referenced_fields=[{
            "category_id": reimbursement_id,
            "category_name": "REIMBURSEMENT_APPLICATION",
            "fields": [
                {"field_id": reimbursement_fields[name], "field_name": name}
                for name in [
                    "Applicant", "Expense Date", "Expense Item",
                    "Requested Payment Amount",
                ]
            ],
            "tables": [],
        }],
    )

    amount_group = client.review.create_group(
        workspace_id=workspace_id,
        repo_id=repo_id,
        name="Cross-document Amount Validation",
    )
    client.review.create_rule(
        workspace_id=workspace_id,
        repo_id=int(repo_id),
        group_id=amount_group.group_id,
        name="Cross-document Amount Match",
        prompt=(
            "Verify that the travel expense amount, hotel total, and payment "
            "amount match within 0.1."
        ),
        category_ids=[reimbursement_id, hotel_id, payment_id],
        risk_level=10,
        referenced_fields=[
            {
                "category_id": reimbursement_id,
                "category_name": "REIMBURSEMENT_APPLICATION",
                "fields": [{
                    "field_id": reimbursement_fields["Travel Expense Amount"],
                    "field_name": "Travel Expense Amount",
                }],
                "tables": [],
            },
            {
                "category_id": hotel_id,
                "category_name": "HOTEL_RECEIPT",
                "fields": [{
                    "field_id": hotel_fields["Total Amount"],
                    "field_name": "Total Amount",
                }],
                "tables": [{
                    "table_id": hotel_table.table_id,
                    "table_name": "Charge Details",
                    "fields": [{
                        "field_id": hotel_table_fields["Amount"],
                        "field_name": "Amount",
                    }],
                }],
            },
            {
                "category_id": payment_id,
                "category_name": "PAYMENT_RECORD",
                "fields": [{
                    "field_id": payment_fields["Transaction Amount"],
                    "field_name": "Transaction Amount",
                }],
                "tables": [],
            },
        ],
    )
    print(f"  Review repository configured: {repo_id}")

    print_step(6, "Submit a review task")
    review_task = client.review.submit_task(
        workspace_id=workspace_id,
        name=f"Expense_Review_{datetime.now():%H%M%S}",
        repo_id=repo_id,
        extract_task_ids=task_ids,
        model=ReviewModel.DEEPSEEK_R1,
    )
    review_task_id = review_task["task_id"]
    print(f"  Review task submitted: {review_task_id}")

    print_step(7, "Wait for the review result")
    for elapsed in range(0, 120, 5):
        result = client.review.get_task_result(
            workspace_id=workspace_id,
            task_id=review_task_id,
        )
        if result.get("status") in (1, 2, 4, 7):
            stats = result.get("statistics", {})
            print(f"  Review completed with status {result.get('status')}")
            print(f"  Passed: {stats.get('pass_count', 0)}")
            print(f"  Failed: {stats.get('failure_count', 0)}")
            print(f"  Errors: {stats.get('error_count', 0)}")
            break
        print(f"  Review still running ({elapsed}s elapsed)")
        time.sleep(5)

    print_section("Quick Start Complete")
    print(f"Workspace ID: {workspace_id}")
    print(f"Review repository ID: {repo_id}")
    print(f"Review task ID: {review_task_id}")


if __name__ == "__main__":
    main()
