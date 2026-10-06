# Changelog

## 0.7.0

- Implement the approved responsive report design with consistent navigation and theme controls.
- Add free optional institution branding through `brand_config`, with embedded local logos and validated palettes.
- Preserve existing capture and assertion APIs, redaction and offline reports.
- Show end time and timezone; open the first request chronologically and preserve failure deep links.


## 0.6.1

- Improve assertion cards, long-content wrapping and responsive spacing.

## 0.3.1

- Correct duplicate Robot Framework wording in the README displayed on PyPI.
- Refresh current version references in installation and configuration documentation.

## 0.3.0

- Rename distribution to robotframework-request-reporter and public import to RequestReporter. Python implementation lives in request_reporter.
- Capture Response and Assert replace the old keyword names, retaining compatibility aliases.
- Test case terminology, structured request URL with copy button, and query parameters preserving duplicate/empty values.
- Live example includes optional metadata; keep the existing 1100 px report width.


## 0.2.0

- Summary, Requests and Failures sections with automatic Robot test names.
- Contextual failed-assertion links and separate unhandled execution errors.
- Assertions terminology, readable UTC date, HTTP method and status-class colors.
- Keyboard navigation for request tabs and focused assertion links.
- Renewed Material documentation, original SVG logo, DataDriver guide and troubleshooting.
- Main integration branch, required pull requests and CI, Pages deployment from main.

## 0.1.1

- Light/dark themes and formatted JSON header copying with manual fallback.

## 0.1.0

- Initial Robot Framework and RequestsLibrary reporter with one HTML per test.
