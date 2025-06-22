# CrawlFused Email Scrapper

This repository provides tools for collecting email addresses from websites.
It includes a basic scraper from `classicalemailscraper` and an asynchronous
crawler built on [Crawlee](https://crawlee.dev/) located in `src/email_crawler3/`.

## Installation

Use a Python 3.11+ environment. Install dependencies from the included
projects:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e crawlee-python
pip install -r classicalemailscraper/requirements.txt
```

## Usage

Run the asynchronous crawler from the repository root:

```bash
python src/email_crawler3/main.py https://example.com
```

Optional arguments:

- `--http-only` – use the HTTP crawler instead of Playwright.
- `--proxy URL` – proxy URL to rotate; can be specified multiple times.
- `--concurrency N` – maximum concurrent requests (default: 5).

The crawler respects `robots.txt`, manages sessions, rotates proxies when
provided and extracts emails using the logic from `classicalemailscraper`.
