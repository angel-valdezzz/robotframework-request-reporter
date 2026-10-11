# Fictional book catalog

Install: `pip install robotframework-request-reporter robotframework-requests`.
Run: `python -m robot --variable REPORT_LANGUAGE:en visual.robot`.
Use `REPORT_LANGUAGE:es` for a Spanish report interface.

The fixture starts a loopback HTTP server and stops it at suite teardown.
Three responses are captured. Four assertions pass; the empty book title causes
one expected failure and exit code 1. Reports are written to the output cases directory.
All content is fictional. No live API, business data, or real credential is used.
