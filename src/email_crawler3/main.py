import argparse
import asyncio
from crawlee.crawlers import PlaywrightCrawler, HttpCrawler
from crawlee import ConcurrencySettings
from crawlee.proxy_configuration import ProxyConfiguration
import importlib.util
import builtins
from pathlib import Path

# Load extract_emails from classicalemailscraper without running its CLI section
_scraper_path = Path(__file__).resolve().parents[1] / ".." / "classicalemailscraper" / "email_scraper.py"
spec = importlib.util.spec_from_file_location("_email_scraper", _scraper_path)
_module = importlib.util.module_from_spec(spec)
_orig_input = builtins.input
builtins.input = lambda *a, **k: (_ for _ in ()).throw(SystemExit)
try:
    spec.loader.exec_module(_module)  # type: ignore[arg-type]
except SystemExit:
    pass
finally:
    builtins.input = _orig_input

extract_emails = _module.extract_emails


async def run_crawler(start_urls: list[str], *, use_playwright: bool = True,
                      proxy_urls: list[str] | None = None, max_concurrency: int = 5) -> set[str]:
    proxy_config = ProxyConfiguration(proxy_urls=proxy_urls) if proxy_urls else None
    crawler_cls = PlaywrightCrawler if use_playwright else HttpCrawler

    concurrency = ConcurrencySettings(max_concurrency=max_concurrency)
    crawler = crawler_cls(
        proxy_configuration=proxy_config,
        use_session_pool=True,
        respect_robots_txt_file=True,
        concurrency_settings=concurrency,
    )

    found_emails: set[str] = set()

    @crawler.router.default_handler
    async def handle_request(context):
        context.log.info(f"Processing {context.request.url}")
        if hasattr(context, "page"):
            body = await context.page.content()
        else:
            body = context.http_response.read().decode()
        found_emails.update(extract_emails(body))
        await context.enqueue_links()

    await crawler.run(start_urls)
    return found_emails


def main() -> None:
    parser = argparse.ArgumentParser(description="Asynchronous email crawler")
    parser.add_argument("start_url", help="URL to start crawling from")
    parser.add_argument("--http-only", action="store_true", help="Use HTTP crawler instead of Playwright")
    parser.add_argument("--proxy", action="append", help="Proxy URL to use. Can be specified multiple times")
    parser.add_argument("--concurrency", type=int, default=5, help="Maximum concurrent requests")
    args = parser.parse_args()

    emails = asyncio.run(
        run_crawler(
            [args.start_url],
            use_playwright=not args.http_only,
            proxy_urls=args.proxy,
            max_concurrency=args.concurrency,
        )
    )

    if emails:
        print("Found emails:")
        for email in sorted(emails):
            print(email)
    else:
        print("No emails found.")


if __name__ == "__main__":
    main()
