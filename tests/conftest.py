from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(monkeypatch):
    isolated_activities = deepcopy(app_module.activities)
    monkeypatch.setattr(app_module, "activities", isolated_activities)

    with TestClient(app_module.app) as test_client:
        yield test_client


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    stats = terminalreporter.stats
    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    errors = len(stats.get("error", []))
    skipped = len(stats.get("skipped", []))
    total = passed + failed + errors + skipped
    status = "PASS" if exitstatus == 0 else "FAIL"

    lines = [
        "# Test Results",
        "",
        f"- Status: **{status}**",
        f"- Total: {total}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Errors: {errors}",
        f"- Skipped: {skipped}",
    ]

    failing_reports = stats.get("failed", []) + stats.get("error", [])
    if failing_reports:
        lines.extend(["", "## Failures", ""])
        for report in failing_reports:
            crash = getattr(report.longrepr, "reprcrash", None)
            message = getattr(crash, "message", "Failure details unavailable")
            lines.append(f"- `{report.nodeid}`: {message}")

    report_path = config.rootpath / "test-results.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")