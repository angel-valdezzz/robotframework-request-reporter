# Request Reporter - Double reading integration

## Approved source

The third demo selected on 2026-10-11:
https://request-reporter-doble-lectura-demo-angel-20261011.candidelf4.chatgpt.site

The integration reuses its five optimized transparent WebP assets and its
responsive composition. The original SVG logo and palette are retained.
The bold white/cyan serif headline reads "La respuesta / no lo cuenta todo."
HTTP 200 remains a small secondary response label.

## Motion and interaction

The pieces open, expose the empty title, and connect it with ASSERTION / FAIL.
The focus lasts 1.5 seconds in a continuous ten-second cycle. There is no hover
pause or speed control. Pause/resume, reduced motion, hidden-tab suspension,
offscreen suspension and instant-navigation teardown are supported.
The hero remains dark independently of the documentation theme.

The lower iframe uses a report regenerated from examples/books/visual.robot,
with three captured responses, four passing assertions and one intentional
empty-title failure. The fixture is loopback-only and needs no external API.
Both report locales and a ZIP of the runnable example are produced at build.
The native Failures link selects request 2 and its exact failed assertion.
Language changes preserve the report section, request, detail tab, filter,
content theme and report section anchor. State is consumed only after the
destination locale and the iframe finish loading.

## Evidence and verification

Browser evidence is generated into build/landing-checks/ by
docs/scripts/verify_landing.py. It checks English and Spanish at 1440x1024,
1366x625, 390x844 and 820x1180, both content themes, overflow, action placement,
continuous motion, real pause/resume, reduced motion, native report navigation,
language round trips, search, instant navigation and JavaScript-free links.
Assertion-focus screenshots capture the empty value and its failed validation.

The strict bilingual build verifies the generated report payload, intentional
failure count, locale and example-secret redaction. Repeated builds replace the
prior generated output. Ruff, mypy and the example Robot format/lint checks pass.

Minor optical differences from the generated concept remain in the system
serif letterforms. The approved moving raster pieces are preserved exactly.
