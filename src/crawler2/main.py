import argparse
import asyncio
from pprint import pprint

from .crawler import crawl_domain

async def run(start_urls, max_pages, concurrency, proxy_urls):
    results = []
    for url in start_urls:
        summary = await crawl_domain(url, max_pages=max_pages, concurrency=concurrency, proxy_urls=proxy_urls)
        results.append(summary)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async email scraper using Crawlee")
    parser.add_argument("start_urls", nargs="+", help="Seed URLs to crawl")
    parser.add_argument("--max-pages", type=int, default=50, dest="max_pages", help="Maximum pages per domain")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent pages")
    parser.add_argument("--proxy", nargs="*", dest="proxy_urls", help="Proxy URLs to rotate")
    args = parser.parse_args()
    summaries = asyncio.run(run(args.start_urls, args.max_pages, args.concurrency, args.proxy_urls))
    pprint(summaries)
