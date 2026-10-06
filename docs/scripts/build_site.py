"""Assemble MkDocs, Libdoc and a generated sample into one Pages artifact."""

import shutil
import subprocess
import sys
from pathlib import Path

from bilingual_libdoc import generate
from bilingual_site import build

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    demo = ROOT / "build" / "report.html"
    if not demo.is_file():
        subprocess.run([sys.executable, str(ROOT / "scripts" / "verify.py")], check=True)
    generate(
        "RequestReporter",
        ROOT,
        "keywords/index.html",
        "https://angel-valdezzz.github.io/robotframework-request-reporter/",
    )
    examples = ROOT / "docs" / "examples"
    examples.mkdir(exist_ok=True)
    shutil.copyfile(demo, examples / "report.html")
    shutil.copyfile(ROOT / "build/report.es.html", examples / "report.es.html")
    # Remove the retired demo even when rebuilding an existing working directory.
    (examples / "skipped.html").unlink(missing_ok=True)
    shutil.copyfile(
        ROOT / "results/acceptance/cases/Passing_distributor.html", examples / "passing.html"
    )
    build(ROOT, ("assets", "examples"))
    print("Built MkDocs, keywords/index.html and examples/report.html.")


if __name__ == "__main__":
    main()
