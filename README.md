# Crawlee Email Scraper

This repository includes an asynchronous email scraping tool powered by the [Crawlee](https://crawlee.dev/) Python library.

## Installation

```bash
# Create and activate a virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e crawlee-python
pip install -r classicalemailscraper/requirements.txt
pip install playwright
playwright install --with-deps chromium
```

## Usage

Run the crawler with one or more seed URLs:

```bash
python -m src.crawler2.main <start_url1> [<start_url2> ...] --max-pages 10
```

Results are stored in local Crawlee datasets under `storage/datasets/`.

## Test Report Example

To reproduce the test crawl used in development:

```bash
python -m src.crawler2.main \
  http://www.mapsoft.com \
  http://www.puzzle.ch \
  http://www.obsmedical.com \
  http://www.mediamelon.com \
  http://www.crosig.hr \
  --max-pages 10
```

After the crawl completes, a summary of pages scraped and deduplicated emails per domain will be printed.
