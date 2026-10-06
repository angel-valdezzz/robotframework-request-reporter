"""Rendered locales preserve secrets protection and caller-owned text."""

import json
import tempfile
import unittest
from pathlib import Path

from request_reporter import RequestReporter
from request_reporter.models import Case
from request_reporter.redaction import Redactor
from request_reporter.render import write_report


class LocaleTests(unittest.TestCase):
    def test_languages_preserve_content_and_redaction(self) -> None:
        case = Case(
            name="Response — caller content",
            source="",
            test_id="t1",
            started="2026-10-01T00:00:00+00:00",
            status="PASS",
            metadata={"token": "private-value", "custom": "Summary"},
        )
        with tempfile.TemporaryDirectory() as tmp:
            for lang, heading, footer in [
                ("en", "Requests overview", "Generated with"),
                ("es", "Resumen de solicitudes", "Generado con"),
            ]:
                path = write_report(case, Path(tmp) / lang, Redactor("", "token"), lang)
                html = path.read_text()
                self.assertIn(f'lang="{lang}"', html)
                self.assertIn(heading, html)
                self.assertIn(footer, html)
                self.assertIn("Response — caller content", html)
                self.assertNotIn("private-value", html)
                payload = html.split('id="case-data">', 1)[1].split("</script>", 1)[0]
                self.assertEqual(json.loads(payload)["metadata"]["custom"], "Summary")
            with self.assertRaisesRegex(ValueError, "INVALID_LANGUAGE"):
                RequestReporter(language="fr")
