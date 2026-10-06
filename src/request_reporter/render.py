"""Render standalone HTML, with a stable JSON payload and no external assets."""

import base64
import re
from dataclasses import asdict
from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, select_autoescape

from .models import Case
from .redaction import Redactor


def write_report(case: Case, directory: Path, redactor: Redactor) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^\w.-]+", "_", case.name, flags=re.UNICODE).strip("._")[:130] or "case"
    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    if stem.split(".", 1)[0].upper() in reserved:
        stem = "test_" + stem
    target = directory / f"{stem}.html"
    counter = 2
    while target.exists():
        target = directory / f"{stem}_{counter}.html"
        counter += 1
    environment = Environment(autoescape=select_autoescape(["html"]))
    template = environment.from_string(
        files("request_reporter").joinpath("templates/report.html").read_text(encoding="utf-8")
    )
    # Final cleaning also removes secrets learned in subsequent requests.
    payload = redactor.clean(asdict(case))
    logo_data = "data:image/svg+xml;base64," + base64.b64encode(
        files("request_reporter").joinpath("assets/logo.svg").read_bytes()
    ).decode("ascii")
    target.write_text(template.render(case=payload, logo_data=logo_data), encoding="utf-8")
    return target
