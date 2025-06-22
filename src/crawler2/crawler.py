from typing import Iterable, List, Dict
from urllib.parse import urlparse

from crawlee import ConcurrencySettings
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.proxy_configuration import ProxyConfiguration
from crawlee.storages import Dataset

from .email_extractor import extract_emails_from_html

async def crawl_domain(start_url: str, *, max_pages: int = 50, concurrency: int = 5,
                       proxy_urls: Iterable[str] | None = None) -> Dict:
    """Crawl a single domain starting from ``start_url``.

    Returns summary statistics with pages scraped and deduplicated emails.
    """
    domain = urlparse(start_url).netloc
    dataset = await Dataset.open(name=f"emails-{domain}")
    await dataset.drop()

    proxy_config = ProxyConfiguration(proxy_urls=list(proxy_urls)) if proxy_urls else None

    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_pages,
        concurrency_settings=ConcurrencySettings(max_concurrency=concurrency),
        proxy_configuration=proxy_config,
        use_session_pool=True,
        respect_robots_txt_file=True,
    )

    @crawler.router.default_handler
    async def handle_page(context: PlaywrightCrawlingContext) -> None:
        await context.page.wait_for_load_state("networkidle")
        html = await context.page.content()
        emails = extract_emails_from_html(html)
        for email in emails:
            await dataset.push_data({"url": context.request.url, "email": email})
        await context.enqueue_links()

    stats = await crawler.run([start_url])

    # Gather dataset results
    items: List[Dict] = []
    offset = 0
    while True:
        page = await dataset.get_data(limit=1000, offset=offset)
        items.extend(page.items)
        if page.total <= offset + page.count:
            break
        offset += page.count

    unique_emails = sorted({it["email"] for it in items})
    page_urls = {it["url"] for it in items}

    return {
        "domain": domain,
        "pages_scraped": stats.requests_finished,
        "deduped_emails": unique_emails,
        "urls_visited": list(page_urls),
    }
