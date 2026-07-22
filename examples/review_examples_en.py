"""English examples for Docflow review repositories, rules, and tasks."""

import os
import time
from datetime import datetime

from dotenv import load_dotenv

from docflow import DocflowClient, ReviewModel


load_dotenv()
client = DocflowClient.from_env()
WORKSPACE_ID = os.getenv("DOCFLOW_WORKSPACE_ID", "123")
REPO_ID = os.getenv("DOCFLOW_REPO_ID", "456")
GROUP_ID = os.getenv("DOCFLOW_GROUP_ID", "789")
RULE_ID = os.getenv("DOCFLOW_RULE_ID", "1001")
TASK_ID = os.getenv("DOCFLOW_REVIEW_TASK_ID", "2001")


def example_create_repo():
    """Example 1: create a review repository."""
    print("\n=== Example 1: Create a review repository ===")
    response = client.review.create_repo(
        workspace_id=WORKSPACE_ID,
        name="Invoice Compliance Rules",
    )
    print(f"Repository created: {response.repo_id}")


def example_list_repos():
    """Example 2: list review repositories."""
    print("\n=== Example 2: List review repositories ===")
    response = client.review.list_repos(
        workspace_id=WORKSPACE_ID,
        page=1,
        page_size=10,
    )
    print(f"Total repositories: {response.total}")
    for repo in response.repos:
        print(f"{repo.repo_id}: {repo.name}")


def example_get_repo():
    """Example 3: get a repository and its nested groups and rules."""
    print("\n=== Example 3: Get a review repository ===")
    repo = client.review.get_repo(workspace_id=WORKSPACE_ID, repo_id=REPO_ID)
    print(f"Repository: {repo.name}")
    for group in repo.groups:
        print(f"  Group: {group.name}")
        for rule in group.rules:
            print(f"    Rule: {rule.name}")


def example_update_repo():
    """Example 4: rename a review repository."""
    print("\n=== Example 4: Update a review repository ===")
    client.review.update_repo(
        workspace_id=WORKSPACE_ID,
        repo_id=REPO_ID,
        name="Updated Invoice Compliance Rules",
    )
    print("Repository updated")


def example_delete_repo():
    """Example 5: delete review repositories."""
    print("\n=== Example 5: Delete review repositories ===")
    client.review.delete_repo(workspace_id=WORKSPACE_ID, repo_ids=[REPO_ID])
    print("Repository deleted")


def example_create_group():
    """Example 6: create a rule group."""
    print("\n=== Example 6: Create a rule group ===")
    response = client.review.create_group(
        workspace_id=WORKSPACE_ID,
        repo_id=REPO_ID,
        name="Amount and Tax Validation",
    )
    print(f"Group created: {response.group_id}")


def example_update_group():
    """Example 7: rename a rule group."""
    print("\n=== Example 7: Update a rule group ===")
    client.review.update_group(
        workspace_id=WORKSPACE_ID,
        group_id=GROUP_ID,
        name="Updated Amount and Tax Validation",
    )
    print("Group updated")


def example_delete_group():
    """Example 8: delete a rule group."""
    print("\n=== Example 8: Delete a rule group ===")
    client.review.delete_group(workspace_id=WORKSPACE_ID, group_id=GROUP_ID)
    print("Group deleted")


def example_create_rule():
    """Example 9: create a basic review rule."""
    print("\n=== Example 9: Create a review rule ===")
    response = client.review.create_rule(
        workspace_id=WORKSPACE_ID,
        repo_id=int(REPO_ID),
        group_id=GROUP_ID,
        name="Invoice Amount Range",
        prompt="Verify that the invoice amount is between 1 and 100,000.",
        risk_level=10,
    )
    print(f"Rule created: {response.rule_id}")


def example_create_rule_with_referenced_fields():
    """Example 10: create a rule that references extracted fields."""
    print("\n=== Example 10: Create a rule with field references ===")
    response = client.review.create_rule(
        workspace_id=WORKSPACE_ID,
        repo_id=int(REPO_ID),
        group_id=GROUP_ID,
        name="Tax Calculation Accuracy",
        prompt="Verify Tax Amount = Net Amount × Tax Rate within 0.01.",
        category_ids=["101"],
        risk_level=10,
        referenced_fields=[{
            "category_id": "101",
            "category_name": "VAT_INVOICE",
            "fields": [
                {"field_id": "1001", "field_name": "Net Amount"},
                {"field_id": "1002", "field_name": "Tax Rate"},
                {"field_id": "1003", "field_name": "Tax Amount"},
            ],
            "tables": [],
        }],
    )
    print(f"Rule created: {response.rule_id}")


def example_create_rule_with_table_fields():
    """Example 11: create a rule that references table columns."""
    print("\n=== Example 11: Create a rule with table references ===")
    response = client.review.create_rule(
        workspace_id=WORKSPACE_ID,
        repo_id=int(REPO_ID),
        group_id=GROUP_ID,
        name="Line-item Amount Total",
        prompt="Verify that all line-item amounts add up to the invoice total.",
        category_ids=["101"],
        risk_level=20,
        referenced_fields=[{
            "category_id": "101",
            "category_name": "VAT_INVOICE",
            "fields": [{"field_id": "1001", "field_name": "Total Amount"}],
            "tables": [{
                "table_id": "5001",
                "table_name": "Line Items",
                "fields": [
                    {"field_id": "5101", "field_name": "Unit Price"},
                    {"field_id": "5102", "field_name": "Quantity"},
                    {"field_id": "5103", "field_name": "Amount"},
                ],
            }],
        }],
    )
    print(f"Rule created: {response.rule_id}")


def example_update_rule():
    """Example 12: update a review rule."""
    print("\n=== Example 12: Update a review rule ===")
    client.review.update_rule(
        workspace_id=WORKSPACE_ID,
        rule_id=RULE_ID,
        name="Updated Invoice Amount Range",
        prompt="Verify that the invoice amount is between 1 and 200,000.",
        risk_level=20,
        category_ids=["101", "102"],
    )
    print("Rule updated")


def example_delete_rule():
    """Example 13: delete a review rule."""
    print("\n=== Example 13: Delete a review rule ===")
    client.review.delete_rule(workspace_id=WORKSPACE_ID, rule_id=RULE_ID)
    print("Rule deleted")


def example_submit_task():
    """Example 14: submit a review task for extraction task IDs."""
    print("\n=== Example 14: Submit a review task ===")
    result = client.review.submit_task(
        workspace_id=WORKSPACE_ID,
        name=f"Invoice Review {datetime.now():%Y-%m-%d}",
        repo_id=REPO_ID,
        extract_task_ids=["3001", "3002"],
        model=ReviewModel.DEEPSEEK_R1,
    )
    print(f"Review task submitted: {result['task_id']}")


def example_submit_task_by_batch():
    """Example 15: submit a review task for one upload batch."""
    print("\n=== Example 15: Submit a review task by batch ===")
    result = client.review.submit_task(
        workspace_id=WORKSPACE_ID,
        name="Batch Review",
        repo_id=REPO_ID,
        batch_number="202607220001",
    )
    print(f"Review task submitted: {result['task_id']}")


def example_get_task_result():
    """Example 16: inspect a detailed review result."""
    print("\n=== Example 16: Get a review task result ===")
    result = client.review.get_task_result(
        workspace_id=WORKSPACE_ID,
        task_id=TASK_ID,
        with_task_detail_url=True,
    )
    print(f"Task: {result.get('task_name')}")
    print(f"Status: {result.get('status')}")
    if result.get("task_detail_url"):
        print(f"Task details: {result['task_detail_url']}")
    stats = result.get("statistics", {})
    print(f"Passed: {stats.get('pass_count', 0)}")
    print(f"Failed: {stats.get('failure_count', 0)}")
    print(f"Errors: {stats.get('error_count', 0)}")
    for group in result.get("review_groups", []):
        print(f"  Group: {group.get('group_name')}")
        for task in group.get("review_tasks", []):
            print(f"    Rule: {task.get('rule_name')}")
            print(f"    Result: {task.get('review_result')}")
            print(f"    Reasoning: {task.get('reasoning', 'N/A')}")


def example_get_task_result_simple():
    """Example 17: display a concise review summary."""
    print("\n=== Example 17: Get a concise review result ===")
    result = client.review.get_task_result(
        workspace_id=WORKSPACE_ID,
        task_id=TASK_ID,
    )
    stats = result.get("statistics", {})
    print(f"Task: {result.get('task_name')}")
    print(f"Status: {result.get('status')}")
    print(
        f"Passed/failed: {stats.get('pass_count', 0)}/"
        f"{stats.get('failure_count', 0)}"
    )


def example_retry_task():
    """Example 18: retry a complete review task."""
    print("\n=== Example 18: Retry a review task ===")
    client.review.retry_task(workspace_id=WORKSPACE_ID, task_id=TASK_ID)
    print("Review task resubmitted")


def example_retry_task_rule():
    """Example 19: retry one rule in a review task."""
    print("\n=== Example 19: Retry one task rule ===")
    client.review.retry_task_rule(
        workspace_id=WORKSPACE_ID,
        task_id=TASK_ID,
        rule_id=RULE_ID,
    )
    print("Rule resubmitted")


def example_delete_task():
    """Example 20: delete review tasks."""
    print("\n=== Example 20: Delete review tasks ===")
    client.review.delete_task(workspace_id=WORKSPACE_ID, task_ids=[TASK_ID])
    print("Review task deleted")


def example_complete_review_workflow():
    """Example 21: create rules, submit a task, and poll its result."""
    print("\n=== Example 21: Complete review workflow ===")
    repo = client.review.create_repo(
        workspace_id=WORKSPACE_ID,
        name="End-to-end Invoice Review",
    )
    group = client.review.create_group(
        workspace_id=WORKSPACE_ID,
        repo_id=repo.repo_id,
        name="Basic Validation",
    )
    client.review.create_rule(
        workspace_id=WORKSPACE_ID,
        repo_id=int(repo.repo_id),
        group_id=group.group_id,
        name="Invoice Number Format",
        prompt="Verify that the invoice number contains exactly eight digits.",
        risk_level=10,
    )
    task = client.review.submit_task(
        workspace_id=WORKSPACE_ID,
        name="End-to-end Review",
        repo_id=repo.repo_id,
        extract_task_ids=["3001"],
    )
    for _ in range(24):
        result = client.review.get_task_result(
            workspace_id=WORKSPACE_ID,
            task_id=task["task_id"],
        )
        if result.get("status") in (1, 2, 4, 7):
            print(f"Review completed with status {result.get('status')}")
            return
        time.sleep(5)
    print("Review did not finish within the example timeout")


def example_review_with_chaining():
    """Example 22: use a workspace-bound review context."""
    print("\n=== Example 22: Chained review calls ===")
    workspace = client.workspace(WORKSPACE_ID)
    repo = workspace.review.create_repo(name="Chained Review Repository")
    group = workspace.review.create_group(
        repo_id=repo.repo_id,
        name="Chained Rule Group",
    )
    rule = workspace.review.create_rule(
        repo_id=int(repo.repo_id),
        group_id=group.group_id,
        name="Chained Rule",
        prompt="Verify the configured business condition.",
    )
    print(f"Created repository {repo.repo_id}, group {group.group_id}, rule {rule.rule_id}")


if __name__ == "__main__":
    print("Docflow review resource examples (English)")
    print("Destructive examples are not run automatically.")
    example_list_repos()
