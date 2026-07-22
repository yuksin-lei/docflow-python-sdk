"""End-to-end Docflow workflow examples (English).

The scenarios demonstrate invoice processing, review automation, and chained
contexts. Replace placeholder IDs and paths before running them against an API.
"""

import os
import time
from datetime import datetime

from dotenv import load_dotenv

from docflow import AuthScope, DocflowClient, ExtractModel


load_dotenv()
client = DocflowClient.from_env()


def scenario_1_invoice_processing():
    """Create an invoice configuration, upload files, and inspect results."""
    print("\n" + "=" * 70)
    print("Scenario 1: Batch Invoice Processing")
    print("=" * 70)

    workspace = client.workspace.create(
        name=f"Invoice Processing {datetime.now():%Y%m%d}",
        auth_scope=AuthScope.PUBLIC,
        description="Workspace for VAT invoice processing",
    )
    workspace_id = workspace.workspace_id
    print(f"Workspace created: {workspace_id}")

    category = client.category.create(
        workspace_id=workspace_id,
        name="VAT_INVOICE",
        extract_model=ExtractModel.Acgpt,
        sample_files=["/path/to/invoice_sample1.pdf"],
        fields=[
            {"name": "Invoice Code", "description": "A 10–12 digit code"},
            {"name": "Invoice Number", "description": "An 8 digit number"},
            {"name": "Invoice Date"},
            {"name": "Buyer Name"},
            {"name": "Buyer Tax ID"},
            {"name": "Seller Name"},
            {"name": "Seller Tax ID"},
            {"name": "Net Amount"},
            {"name": "Tax Rate"},
            {"name": "Tax Amount"},
            {"name": "Total Amount"},
        ],
        tables=[{
            "name": "Line Items",
            "prompt": "Extract every invoice line item.",
            "fields": [
                {"name": "Description"},
                {"name": "Specification"},
                {"name": "Unit"},
                {"name": "Quantity"},
                {"name": "Unit Price"},
                {"name": "Amount"},
            ],
        }],
        category_prompt="A VAT invoice with buyer, seller, tax, and line-item data.",
    )
    print(f"Category created: {category.category_id}")

    invoice_paths = [
        "/path/to/invoices/invoice1.pdf",
        "/path/to/invoices/invoice2.pdf",
        "/path/to/invoices/invoice3.pdf",
    ]
    task_ids = []
    for path in invoice_paths:
        response = client.file.upload(
            workspace_id=workspace_id,
            category="VAT_INVOICE",
            file_path=path,
        )
        task_ids.extend(item.task_id for item in response.files if item.task_id)
        print(f"Uploaded {path}; batch number: {response.batch_number}")

    processed = []
    for attempt in range(12):
        response = client.file.fetch(workspace_id=workspace_id, page_size=100)
        processed = [item for item in response.files if item.task_id in task_ids]
        pending = [item for item in processed if item.recognition_status in (0, 3, 4, 5)]
        print(f"Polling attempt {attempt + 1}: {len(pending)} files pending")
        if not pending and len(processed) == len(task_ids):
            break
        time.sleep(5)

    for item in processed:
        if item.recognition_status == 1:
            print(f"Processed successfully: {item.name}")
        else:
            print(f"Processing failed: {item.name}; reason={item.failure_causes}")

    return workspace_id, category.category_id, task_ids


def scenario_2_invoice_review(workspace_id=None, task_ids=None):
    """Configure invoice checks, submit a review, and display its result."""
    print("\n" + "=" * 70)
    print("Scenario 2: Invoice Compliance Review")
    print("=" * 70)
    workspace_id = workspace_id or os.getenv("DOCFLOW_WORKSPACE_ID", "123")
    task_ids = task_ids or ["3001"]

    repo = client.review.create_repo(
        workspace_id=workspace_id,
        name="Invoice Compliance Repository",
    )
    basic_group = client.review.create_group(
        workspace_id=workspace_id,
        repo_id=repo.repo_id,
        name="Basic Invoice Validation",
    )
    client.review.create_rule(
        workspace_id=workspace_id,
        repo_id=int(repo.repo_id),
        group_id=basic_group.group_id,
        name="Invoice Number Format",
        prompt="Verify that the invoice number contains exactly eight digits.",
        risk_level=10,
    )
    client.review.create_rule(
        workspace_id=workspace_id,
        repo_id=int(repo.repo_id),
        group_id=basic_group.group_id,
        name="Invoice Date Range",
        prompt="Verify that the invoice date is not before 2020 or after today.",
        risk_level=20,
    )

    amount_group = client.review.create_group(
        workspace_id=workspace_id,
        repo_id=repo.repo_id,
        name="Amount Calculation Validation",
    )
    client.review.create_rule(
        workspace_id=workspace_id,
        repo_id=int(repo.repo_id),
        group_id=amount_group.group_id,
        name="Tax Calculation Accuracy",
        prompt="Verify Tax Amount = Net Amount × Tax Rate within 0.01.",
        risk_level=10,
    )
    client.review.create_rule(
        workspace_id=workspace_id,
        repo_id=int(repo.repo_id),
        group_id=amount_group.group_id,
        name="Total Amount Accuracy",
        prompt="Verify Total Amount = Net Amount + Tax Amount within 0.01.",
        risk_level=10,
    )

    task = client.review.submit_task(
        workspace_id=workspace_id,
        name=f"Invoice Review {datetime.now():%Y%m%d%H%M%S}",
        repo_id=repo.repo_id,
        extract_task_ids=task_ids,
    )
    print(f"Review task submitted: {task['task_id']}")

    for attempt in range(24):
        result = client.review.get_task_result(
            workspace_id=workspace_id,
            task_id=task["task_id"],
            with_task_detail_url=True,
        )
        if result.get("status") in (1, 2, 4, 7):
            stats = result.get("statistics", {})
            print(f"Review status: {result.get('status')}")
            print(f"Passed: {stats.get('pass_count', 0)}")
            print(f"Failed: {stats.get('failure_count', 0)}")
            print(f"Errors: {stats.get('error_count', 0)}")
            return
        print(f"Review polling attempt {attempt + 1}")
        time.sleep(5)


def scenario_3_using_chaining():
    """Use bound workspace and category contexts to reduce repeated IDs."""
    print("\n" + "=" * 70)
    print("Scenario 3: Chained Context Calls")
    print("=" * 70)
    workspace_id = os.getenv("DOCFLOW_WORKSPACE_ID", "123")
    category_id = os.getenv("DOCFLOW_CATEGORY_ID", "456")

    workspace = client.workspace(workspace_id)
    detail = workspace.get()
    print(f"Workspace: {detail.name}")

    category = workspace.category(category_id)
    field = category.fields.add(
        name="Notes",
        description="Additional invoice notes",
    )
    print(f"Field created: {field.field_id}")
    print(f"Fields in category: {len(category.fields.list().fields)}")
    print(f"Tables in category: {len(category.tables.list().tables)}")

    repo = workspace.review.create_repo(name="Chained Review Repository")
    group = workspace.review.create_group(
        repo_id=repo.repo_id,
        name="Chained Rule Group",
    )
    rule = workspace.review.create_rule(
        repo_id=int(repo.repo_id),
        group_id=group.group_id,
        name="Required Notes Check",
        prompt="Verify the Notes field according to the business policy.",
    )
    print(f"Created review rule: {rule.rule_id}")


if __name__ == "__main__":
    print("Docflow complete workflow examples (English)")
    print("Choose a scenario and replace placeholder values before execution.")
    scenario_3_using_chaining()
