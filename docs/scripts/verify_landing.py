"""Check the published layout, motion controls and localized navigation in Chromium."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT / "site"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/"
    output = ROOT / "build/landing-checks"
    output.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=["--no-sandbox"])
            for lang in ("en", "es"):
                for width in (390, 1440):
                    page = browser.new_page(viewport={"width": width, "height": 1000})
                    errors: list[str] = []
                    page.on("pageerror", lambda error, found=errors: found.append(str(error)))
                    url = base + ("es/" if lang == "es" else "")
                    page.goto(url)
                    page.locator("[data-er-pause]").wait_for(state="visible")
                    assert page.locator("[data-er-hero]").get_attribute("data-lang") == lang
                    assert page.locator("h1").count() == 1
                    assert page.locator(".er-scene-title img").bounding_box()["width"] <= 40
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                    page.locator("[data-er-pause]").click()
                    assert page.locator("[data-er-pause]").inner_text() == (
                        "Reanudar" if lang == "es" else "Resume"
                    )
                    before = page.locator(".er-assemble.is-visible").count()
                    page.wait_for_timeout(500)
                    assert page.locator(".er-assemble.is-visible").count() == before
                    page.locator("[data-er-replay]").click()
                    page.wait_for_timeout(10000)
                    assert (
                        page.locator(".er-assemble.is-visible").count()
                        == page.locator(".er-assemble").count()
                    )
                    page.evaluate("scrollTo(0, 0)")
                    page.wait_for_timeout(400)
                    for scheme in ("default", "slate"):
                        page.evaluate(
                            "scheme => document.body.setAttribute('data-md-color-scheme', scheme)",
                            scheme,
                        )
                        page.screenshot(
                            path=str(output / f"{lang}-{width}-{scheme}.png"), full_page=True
                        )
                    demo = page.locator(".er-action-secondary").get_attribute("href")
                    assert demo
                    response = page.request.get(
                        page.locator(".er-action-secondary").evaluate("el => el.href")
                    )
                    assert response.ok
                    page.locator(".er-action-primary").click()
                    page.wait_for_function("!document.querySelector('[data-er-hero]')")
                    page.go_back()
                    page.locator("[data-er-pause]").wait_for(state="visible")
                    page.locator("[data-er-pause]").click()
                    assert page.locator("[data-er-pause]").get_attribute("aria-pressed") == "true"
                    page.emulate_media(reduced_motion="reduce")
                    assert page.locator("[data-er-pause]").is_disabled()
                    assert (
                        page.locator(".er-assemble.is-visible").count()
                        == page.locator(".er-assemble").count()
                    )
                    assert not errors, errors
                    page.close()
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(base)
            assert page.locator(".er-animation-controls").is_hidden()
            assert all(stage.is_visible() for stage in page.locator(".er-assemble").all())
            browser.close()
    finally:
        server.shutdown()
    print("Landing checks passed: EN/ES, mobile/desktop, themes, motion and navigation.")


if __name__ == "__main__":
    main()
