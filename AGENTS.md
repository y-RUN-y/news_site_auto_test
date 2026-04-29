Yes: Read README*, root manifests, and workspace config first to understand project layout.
Yes: Check pyproject.toml and poetry.lock to know dependencies and Python version constraints.
Yes: Review pytest config and Playwright settings in pyproject.toml to know how tests run and how browsers are launched.
Yes: Identify the real entrypoints (run.py and test_cases) to understand test orchestration.
Yes: Determine monorepo boundaries and major directories (pages, test_cases, utils, report) and ownership.
Yes: Understand how to run a single test or a focused verification step (pytest path::test_name).
Yes: Use or register test markers to support selective test runs.
Yes: Understand cross-page flow patterns in this repo (POM with page objects returning next page objects).
Yes: Decide how new-tab vs same-tab results are handled in tests (window handling utilities).
Yes: Look for data-driven test patterns (data/ folder, conftest fixtures) to extend coverage.
Yes: Be aware of Allure reporting paths and cleaning behavior between runs.
Yes: Ensure environment setup steps (poetry install, playwright install) are followed in local/CI.
Yes: Use the repo's instruction files (AGENTS.md, CLAUDE.md, .cursor/rules/, .cursorrules, .github/copilot-instructions.md) as authoritative references, not ad-hoc notes.
Yes: When adding tests, prefer markers like newcase for incremental runs, and keep test data in data/ to separate data from tests.
