"""Generate and verify the real bilingual book report used by the landing page."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile


def build_book_example(root: Path, destination: Path) -> None:
    source = root / "examples/books"
    for language in ("en", "es"):
        output = root / "build/books" / language
        if output.exists():
            shutil.rmtree(output)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "robot",
                "--outputdir",
                str(output),
                "--variable",
                f"REPORT_LANGUAGE:{language}",
                str(source / "visual.robot"),
            ],
            cwd=root,
            check=False,
        )
        if result.returncode != 1:
            raise ValueError(f"Book example must fail exactly once: {result.returncode}")
        reports = list((output / "cases").glob("*.html"))
        if len(reports) != 1:
            raise ValueError(f"Expected one book report, found {len(reports)}")
        html = reports[0].read_text(encoding="utf-8")
        match = re.search(r'id="case-data">(.*?)</script>', html, re.DOTALL)
        if match is None:
            raise ValueError("Book report has no case payload")
        case = json.loads(match[1])
        checks = [item for exchange in case["exchanges"] for item in exchange["validations"]]
        failed = [item for item in checks if item["status"] == "FAIL"]
        if (
            case["status"] != "FAIL"
            or len(case["exchanges"]) != 3
            or sum(item["status"] == "PASS" for item in checks) != 4
            or len(failed) != 1
            or failed[0]["label"] != "Book title must contain a value"
            or case["exchanges"][2]["response_body"]["title"] != ""
            or case["execution_errors"]
            or "fake-book-SECRET" in html
            or f'lang="{language}"' not in html
        ):
            raise ValueError("Book report does not match the landing's actual case")
        shutil.copyfile(reports[0], destination / f"books.{language}.html")
    with ZipFile(destination / "book-example.zip", "w") as archive:
        for filename in ("Fixture.py", "visual.robot", "README.md"):
            archive.write(source / filename, arcname=f"books/{filename}")
