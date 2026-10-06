"""Institution branding is portable and never changes recorded data or semantic states."""

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from request_reporter.branding import load_branding


class BrandingTests(unittest.TestCase):
    def test_relative_logo_and_accessible_palette(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Image.new("RGB", (900, 300), "#164e63").save(root / "logo.png")
            config = root / "brand.json"
            config.write_text(
                json.dumps(
                    {
                        "name": "Institution <QA>",
                        "logo": "logo.png",
                        "palette": {"primary": "#164e63"},
                    }
                )
            )
            brand = load_branding(config)
            self.assertEqual(brand["name"], "Institution <QA>")
            self.assertTrue(brand["logo_data"].startswith("data:image/png;base64,"))
            self.assertEqual(brand["palette"]["primary"], "#164e63")
            from io import BytesIO

            with Image.open(BytesIO(brand["logo_bytes"])) as image:
                self.assertEqual(image.size, (512, 171))

    def test_invalid_and_low_contrast_configuration_is_rejected(self):
        for config in (
            {"palette": {"primary": "#ffffff"}},
            {"palette": {"primary_dark": "#151d32"}},
            {"palette": {"primary": "red;display:none"}},
            {"palette": {"fail": "#164e63"}},
            {"name": ""},
            {"extra": True},
        ):
            with (
                self.subTest(config=config),
                self.assertRaisesRegex(ValueError, "INVALID_BRANDING"),
            ):
                load_branding(config)

    def test_brand_does_not_bypass_redaction_or_html_escaping(self):
        from request_reporter.models import Case
        from request_reporter.redaction import Redactor
        from request_reporter.render import write_report

        with tempfile.TemporaryDirectory() as tmp:
            case = Case("Case <script>", "", "1", "2026-10-06T18:00:00+00:00", status="FAIL")
            path = write_report(
                case,
                Path(tmp),
                Redactor("authorization", "password"),
                brand_config={"name": "Institution <script>"},
            )
            html = path.read_text()
            self.assertIn("Institution &lt;script&gt;", html)
            self.assertIn("FAIL", html)
            self.assertEqual(case.metadata, {})
