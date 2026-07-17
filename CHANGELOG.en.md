# Changelog

[简体中文](CHANGELOG.md) | [English](CHANGELOG.en.md)

This document records all notable changes to the Docflow Python SDK.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-07-02

### Added

- ✨ **Extract model V1.6 names and the new Auto model** (aligned with backend v2.11.0)
  - Added `ExtractModel.Auto` (intelligent field-level routing), `Acgpt`, `Acgpt_VL`, and `DF_M1`.
  - In `Auto` mode, the algorithm selects the model used for each request.
  - `Acgpt-VL` is a multimodal model intended for straightforward extraction of documents up to 10 pages.

### Changed

- 🔤 Renamed extract models: `Model 1 → Acgpt`, `Model 2 → DF-M1`, and `Model 3 → Acgpt-VL`.
- ✅ Relaxed `extract_model` validation in `category.create/update`, `tables.add/update`, and `fields.add/update` to accept all new names while retaining old-name compatibility.
- 📄 Field and table entries returned by `/file/fetch` now pass through `configModel` and `hitModelReason` under `FileInfo.data`.

### Deprecated

- ⚠️ `ExtractModel.Model_1`, `Model_2`, and `Model_3` are deprecated. They remain as compatibility aliases and are still accepted by the backend; migrate to the new names.

## [1.0.5] - 2026-06-01

### Added

- ✨ **One-step category creation**
  - Added the `tables` parameter to `category.create`, including support for embedded table fields.
- ✨ **Batch field operations**
  - Added `CategoryFieldResource.batch_add()` and `batch_update()` for regular and table fields.
- ✨ **Batch table operations**
  - Added `CategoryTableResource.batch_add()` and `batch_update()` with embedded field definitions.
- ✨ **Batch sample operations**
  - Added `CategorySampleResource.batch_upload()` for up to 20 files and `batch_download()` for ZIP archives.
- ✨ **`with_detail` support**
  - Batch create and update operations can return complete object details with `with_detail=True`.
- ✨ **Enhanced response models**
  - Expanded `CategoryCreateResponse`, `SampleUploadResponse`, `FieldAddResponse`, and `TableAddResponse`.
  - Added `BatchFieldAddResponse`, `BatchTableAddResponse`, and `BatchSampleUploadResponse`.
- ✨ **Context API updates**
  - Added batch methods to `CategoryFieldContext`, `CategoryTableContext`, and `CategorySampleContext`.
  - Added `tables` support to `WorkspaceContext.create_category()`.

### Fixed

- 🐛 Fixed boolean parsing where an `or` expression incorrectly discarded `False`; parsing now uses the `_get_first` helper.

### Compatibility

- ⚡ All new inputs are optional and preserve previous default behavior.
- ⚡ Existing user code continues to work without changes.

---

## [1.0.3] - 2026-04-28

### Added

- ✨ Added the `ReviewModel` enum for review model selection:
  - `DEEPSEEK_R1 = "1"`: deepseek-r1
  - `QWQ_32B = "2"`: qwq-32b
  - `QWEN3_MAX = "3"`: qwen3-max
  - `ORM_O1 = "5"`: ORM-O1
- Added the optional `model` parameter to `client.review.submit_task()` and `client.review.get_task_result()`.

---

## [1.0.0] - 2026-03-17

### Added

#### Core features

- ✨ **Workspace management (`WorkspaceResource`)**
  - Create, list, fetch, update, and batch-delete workspaces.
  - Iterate through all workspaces with automatic pagination.
- ✨ **Category management (`CategoryResource`)**
  - Create categories with LLM/VLM extraction models.
  - List, fetch, update, batch-delete, and iterate through categories.
- ✨ **Field management (`FieldContext`)**
  - List, add, configure, update, and batch-delete category fields.
- ✨ **Table management (`TableContext`)**
  - List, add, update, and batch-delete tables and their fields.
- ✨ **Sample management (`SampleContext`)**
  - Upload from paths or file objects, list, download, and batch-delete samples.
  - Parse standard and RFC 5987 `Content-Disposition` filenames and decode internationalized filenames.
- ✨ **File processing (`FileResource`)**
  - Asynchronous and synchronous upload.
  - Fetch and iterate through processed files.
  - Single and batch updates, flexible deletion, additional extraction, retries, and category amendment.
- ✨ **Review management (`ReviewResource`)**
  - Create, list, fetch, update, and delete review repositories.
  - Create, update, and delete rule groups and rules.
  - Submit, query, retry, and delete review tasks; retry individual rules.

#### Contexts and chained calls

- ✨ Added `WorkspaceContext`, `CategoryContext`, and `ReviewContext`.
- Contexts bind `workspace_id` and `category_id` automatically and expose the corresponding resource methods.
- Chained usage includes `client.workspace("ws_id").category("cat_id")` and `client.workspace("ws_id").review`.

#### Data models

- ✨ Added workspace response and information models.
- ✨ Added category response and information models.
- ✨ Added field, table, and sample response and information models.
- ✨ Added file upload, fetch, update, and deletion models.
- ✨ Added review repository, group, rule, and task models.
- ✨ All models support `from_dict()` and accept both camelCase and snake_case keys.

#### Internationalization

- ✨ Added parameterized error messages in Simplified Chinese (`zh_CN`) and English (`en_US`).
- Added constructor-time, dynamic, and global language selection.
- Added methods to query the active and available languages.

#### Exception handling

- ✨ Added a structured exception hierarchy for validation, authentication, authorization, not-found, conflict, rate-limit, server, network, timeout, and API errors.
- Exceptions expose useful request and response context where available.

#### HTTP client

- ✨ Added a reusable HTTP session with a connection pool of 10 pools and up to 20 connections.
- ✨ Added configurable retry status codes, methods, counts, and exponential backoff.
- ✨ Added configurable connection and read timeouts.
- ✨ Added JSON and multipart request handling plus consistent response/error parsing.

#### Utilities

- ✨ Added file validation, size checks, MIME type handling, multipart helpers, response mapping, and internationalized filename parsing.

#### Enums

- ✨ Added enums for authentication scope, enabled state, extraction model, field type, mismatch action, processing status, and review configuration.

#### Authentication and security

- ✨ Added `x-ti-app-id` and `x-ti-secret-code` header authentication.
- ✨ Added environment-variable configuration and safe handling that avoids exposing credentials in logs and exceptions.

#### Developer experience

- ✨ Added complete type annotations, docstrings, IDE-friendly exports, Pythonic resource APIs, context managers, and automatic resource cleanup.

#### Tests

- ✨ Added unit and integration coverage for resources, models, exceptions, retries, internationalization, chained calls, pagination, uploads, and response parsing.
- ✨ Added fixtures and mocks for isolated API testing.

#### Documentation

- ✨ Added installation, quick-start, API, configuration, internationalization, retry, security, and release documentation.
- ✨ Added examples for file processing, review resources, and end-to-end workflows.

#### Configuration and constants

- ✨ Added defaults for the API endpoint, API version, timeouts, connection pools, retry behavior, pagination, supported file types, and file-size limits.
- ✨ Added environment-variable overrides for credentials, endpoint, timeouts, retries, pool settings, and language.

#### Dependency management

- ✨ Added runtime dependencies for HTTP requests, retry handling, and typing compatibility.
- ✨ Added development dependencies for testing, coverage, formatting, linting, and type checking.

### Changed

- Established the first stable public API and package layout.
- Standardized naming, model conversion, validation, and error handling across resources.

### Fixed

- Addressed initial response parsing, filename decoding, pagination, connection reuse, and error mapping issues found during stabilization.

### Security

- Credentials are sent through authentication headers and are excluded from diagnostic output.
- HTTPS is used by the default API endpoint.

---

## Versioning Notes

### Version format

Versions use `MAJOR.MINOR.PATCH`:

- **MAJOR**: incompatible API changes
- **MINOR**: backward-compatible functionality
- **PATCH**: backward-compatible bug fixes

### Change categories

- **Added**: new functionality
- **Changed**: changes to existing functionality
- **Deprecated**: functionality scheduled for removal
- **Removed**: removed functionality
- **Fixed**: bug fixes
- **Security**: security-related changes
- **Compatibility**: compatibility notes
