"""Run Robot acceptance tests and verify intentional failures and report isolation."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from robot.api import ExecutionResult

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        cwd=ROOT,
        check=True,
    )
    output = ROOT / "results" / "acceptance"
    if output.exists():
        shutil.rmtree(output)
    process = subprocess.run(
        [sys.executable, "-m", "robot", "--outputdir", str(output), str(ROOT / "tests")],
        cwd=ROOT,
        check=False,
    )
    from robot.libdocpkg import LibraryDocumentation

    keywords = {kw.name for kw in LibraryDocumentation("RequestReporter").keywords}
    assert keywords == {
        "Assert",
        "Capture Response",
        "Set Case Metadata",
        "Capture Request Error",
    }, keywords
    result = ExecutionResult(str(output / "output.xml"))
    tests = [test for suite in result.suite.suites for test in suite.tests]
    assert len(tests) == 19, f"Expected 19 cases, got {len(tests)}"
    for test in tests:
        if "expected-failure" in test.tags:
            assert test.status == "FAIL", f"Expected intentional failure: {test.name}"
        elif test.name == "Skipped case":
            assert test.status == "SKIP"
        else:
            assert test.status == "PASS", f"{test.name}: {test.message}"
    assert all(s.teardown.status == "PASS" for s in result.suite.suites)
    assert process.returncode == 7, f"Unexpected Robot exit code: {process.returncode}"
    reports = list((output / "cases").glob("*.html"))
    assert len(reports) == 19, "One report per test, including duplicate names and SKIP"
    for path in reports:
        html = path.read_text(encoding="utf-8")
        match = re.search(
            r'<script type="application/json" id="case-data">(.*?)</script>', html, re.DOTALL
        )
        assert match, f"Missing report payload: {path}"
        data = json.loads(match[1])
        assert data["status"] != "RUNNING"
        assert data["suite"]
        assert "Requests overview" in html
        assert "fixture-token-SECRET" not in html
        assert "fixture-secret-SECRET" not in html
        assert "query-secret-SECRET" not in html
        assert '<script>alert("unsafe")</script>' not in html
        if data["name"] == "Failing distributor":
            query = parse_qsl(urlsplit(data["exchanges"][-1]["url"]).query, keep_blank_values=True)
            assert ("tag", "one") in query and ("tag", "two") in query and ("empty", "") in query
            assert data["metadata"]["case_id"] == "DIST-002"
        errors = data["execution_errors"]
        if data["name"] in {"Failing distributor", "Empty fields", "Handled error"}:
            assert not errors, f"Assertions/handled failures duplicated: {data['name']}"
        if data["name"] == "Invalid JSON stops parsing":
            assert len(errors) == 1 and "JSON" in errors[0]["message"]
        if data["name"] == "Timeout without response":
            assert len(errors) == 1 and not data["exchanges"]
            assert "Timeout" in errors[0]["message"] or "timed out" in errors[0]["message"]
        if data["name"] == "CON":
            assert path.name == "test_CON.html"
        if data["name"] == "Captured timeout without response":
            assert not data["exchanges"]
            assert len(data["request_errors"]) == 1
            attempt = data["request_errors"][0]
            assert attempt["method"] == "GET" and ("api_key", "[REDACTED]") in parse_qsl(
                urlsplit(attempt["url"]).query
            )
            assert "status_code" not in attempt and "response_body" not in attempt
        if data["name"] == "Empty fields":
            assert all(v["expected"] is None for v in data["exchanges"][0]["validations"])
        if data["name"] == "Handled error then unhandled error":
            assert len(errors) == 1
            assert errors[0]["message"] == "Unhandled failure must appear"
    from request_reporter.models import Case, Exchange, ExecutionError, RequestError, Validation
    from request_reporter.redaction import Redactor
    from request_reporter.render import write_report

    spanish = output / "cases-es"
    spanish.mkdir()
    for path in reports:
        payload = json.loads(
            re.search(
                r'<script type="application/json" id="case-data">(.*?)</script>',
                path.read_text(),
                re.DOTALL,
            )[1]
        )
        payload["exchanges"] = [
            Exchange(
                **{**exchange, "validations": [Validation(**v) for v in exchange["validations"]]}
            )
            for exchange in payload["exchanges"]
        ]
        payload["execution_errors"] = [ExecutionError(**e) for e in payload["execution_errors"]]
        payload["request_errors"] = [RequestError(**e) for e in payload["request_errors"]]
        rendered = write_report(Case(**payload), spanish, Redactor("", ""), "es")
        rendered.rename(spanish / path.name)
    failing = next(p for p in reports if p.name == "Failing_distributor.html")
    demo = ROOT / "build" / "report.html"
    demo.parent.mkdir(exist_ok=True)
    shutil.copyfile(failing, demo)
    shutil.copyfile(spanish / failing.name, ROOT / "build" / "report.es.html")
    print("Verified 19 Robot cases, assertion/execution errors, DataDriver and redaction.")


if __name__ == "__main__":
    main()
