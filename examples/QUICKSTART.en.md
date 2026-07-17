# Quick Start — Expense Reimbursement

[简体中文](QUICKSTART.md) | [English](QUICKSTART.en.md)

This guide walks through an end-to-end expense document processing and review workflow using the Docflow SDK.

## 🎯 Scenario

Finance teams commonly process several document types for one reimbursement request:

- **Expense claim** (XLS): applicant, business-trip purpose, and expense details
- **Hotel folio** (image): check-in and check-out dates plus itemized charges
- **Payment record** (image or PDF): transaction number, amount, payer, and payee

Docflow can automate:

1. Document classification
2. Structured information extraction
3. Intelligent rule-based review

## 📋 Prerequisites

### 1. Install the SDK

```bash
pip install docflow-sdk
```

### 2. Obtain credentials

Sign in to the [TextIn console](https://www.textin.com/console/dashboard/setting) and obtain:

- `x-ti-app-id`
- `x-ti-secret-code`

Keep these values in environment variables or a secrets manager. Never hard-code or commit them.

### 3. Prepare sample files

Download the repository samples or use your own reimbursement documents under `sample_files/`:

```text
sample_files/
├── 报销申请单.XLS
├── sample_hotel_receipt.png
└── sample_payment_record.pdf
```

Repository samples are available in `examples/sample_files/`.

### 4. Configure environment variables

```bash
export DOCFLOW_APP_ID="your-app-id"
export DOCFLOW_SECRET_CODE="your-secret-code"
export DOCFLOW_BASE_URL="https://docflow.textin.com/api"
```

If your application uses a local `.env` file, load it without committing it:

```python
from dotenv import load_dotenv
import os

load_dotenv()

client = DocflowClient(
    base_url=os.getenv("DOCFLOW_BASE_URL"),
    app_id=os.getenv("DOCFLOW_APP_ID"),
    secret_code=os.getenv("DOCFLOW_SECRET_CODE"),
)
```

## 🚀 Run the Example

From the repository root:

```bash
cd examples
python quick_start.py
```

The example will:

1. Create a workspace.
2. Configure expense claim, hotel folio, and payment record categories.
3. Upload the documents.
4. Wait for and display extraction results.
5. Configure a review repository with rule groups and rules.
6. Submit a review task.
7. Wait for and display the review result.

Document extraction and review can each take approximately 10–30 seconds, depending on document size and service load.

## 📊 Expected Output

Successful output follows this pattern; IDs and extracted values will differ:

```text
======================================================================
  Docflow SDK Quick Start — Expense Reimbursement
======================================================================

[Step 1] Create workspace
  ✓ Workspace created: 123456

[Step 2] Configure document categories
  [2.1] Create expense claim category...
    ✓ Category ID: 789001
  [2.2] Create hotel folio category...
    ✓ Category ID: 789002
    ✓ Added 4 table fields
  [2.3] Create payment record category...
    ✓ Category ID: 789003

[Step 3] Upload documents
  ✓ 报销申请单.XLS -> batch_number: 2024...
  ✓ sample_hotel_receipt.png -> batch_number: 2024...
  ✓ sample_payment_record.pdf -> batch_number: 2024...

[Step 4] Fetch extraction results
  Waiting for processing (usually 10–30 seconds)...
  [1/3] ✓ Expense claim completed
  [2/3] ✓ Hotel folio completed
  [3/3] ✓ Payment record completed

[Step 5] Configure review rules
  ✓ Created 3 rule groups and 5 review rules

[Step 6] Submit review task
  ✓ Review task submitted: 987654

[Step 7] Fetch review result
  ✓ Review completed

Review status: Passed
Rules passed: 5
Rules failed: 0
Rule errors: 0
```

The example checks required fields, reimbursement totals, hotel line-item totals, cross-document amount consistency, and applicant/payer identity consistency.

## 💡 Core Code

### Initialize the client

```python
from docflow import DocflowClient

client = DocflowClient.from_env()
```

### Create a workspace

```python
from docflow import AuthScope

workspace = client.workspace.create(
    name="Expense Reimbursement",
    auth_scope=AuthScope.PUBLIC,
    description="Automated expense document processing",
)
workspace_id = workspace.workspace_id
```

### Configure document categories

```python
from docflow import ExtractModel

category = client.category.create(
    workspace_id=workspace_id,
    name="Expense Claim",
    extract_model=ExtractModel.Acgpt,
    sample_files=["sample_files/报销申请单.XLS"],
    fields=[
        {"name": "Applicant"},
        {"name": "Trip Purpose"},
        {"name": "Requested Amount"},
    ],
)
```

Configure separate categories for the hotel folio and payment record. Table definitions can be embedded in the category's `tables` argument.

### Upload files

```python
response = client.file.upload(
    workspace_id=workspace_id,
    file_path="sample_files/sample_hotel_receipt.png",
)

batch_number = response.batch_number
file_id = response.files[0].id
```

Use `upload_sync()` when the caller should wait for processing to complete automatically.

### Query extraction results

```python
result = client.file.fetch(
    workspace_id=workspace_id,
    file_ids=[file_id],
)

for file_info in result.files:
    print(file_info.name, file_info.status, file_info.data)
```

For multiple pages, use `client.file.iter(workspace_id=workspace_id)`.

### Configure review rules

```python
repo = client.review.create_repo(
    workspace_id=workspace_id,
    name="Expense Compliance Review",
)

group = client.review.create_group(
    workspace_id=workspace_id,
    repo_id=repo.repo_id,
    name="Expense Claim Validation",
)

rule = client.review.create_rule(
    workspace_id=workspace_id,
    repo_id=repo.repo_id,
    group_id=group.group_id,
    name="Required Fields",
    prompt="Verify that all required expense fields are present.",
)
```

Exact rule parameters should match the server configuration and the fields created for each category. See `quick_start.py` for the complete executable definitions.

### Submit a review task

```python
task = client.review.submit_task(
    workspace_id=workspace_id,
    repo_id=repo.repo_id,
    file_ids=[file_id],
)
task_id = task.task_id
```

You can also submit all files associated with a batch where supported.

### Fetch review results

```python
result = client.review.get_task_result(
    workspace_id=workspace_id,
    task_id=task_id,
)

print(result.status)
```

Poll only at a reasonable interval and enforce an application-level timeout when building production workflows.

## 🔄 Workflow

```text
Credentials and sample files
            │
            ▼
     Create workspace
            │
            ▼
 Configure three categories
            │
            ▼
       Upload files
            │
            ▼
 Wait for extraction results
            │
            ▼
 Configure repository, groups,
        and review rules
            │
            ▼
     Submit review task
            │
            ▼
   Wait for review results
            │
            ▼
  Handle pass/fail outcomes
```

## 📚 Next Steps

- Read the main [SDK documentation](../README.en.md).
- Browse the [examples guide](README.en.md).
- Review [file_examples.py](file_examples.py) for file operations.
- Review [review_examples.py](review_examples.py) for review resources.
- Review [complete_workflow_example.py](complete_workflow_example.py) for larger workflows.

## ⚠️ Notes

- Example execution creates server-side workspaces, categories, rules, and tasks. Reuse or clean them up as appropriate.
- Processing time varies with document size, page count, and service load.
- Verify extracted and reviewed data before using it for financial decisions.
- Use representative, non-sensitive samples during development.
- Keep credentials out of source code, logs, screenshots, and committed `.env` files.

## 📄 License

See [LICENSE](../LICENSE) for license information.
