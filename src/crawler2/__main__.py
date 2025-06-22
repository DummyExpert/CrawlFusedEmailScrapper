from .main import run

if __name__ == "__main__":
    import argparse
    import asyncio
    parser = argparse.ArgumentParser(description="Async email scraper using Crawlee")
    parser.add_argument("start_urls", nargs="+", help="Seed URLs to crawl")
    parser.add_argument("--max-pages", type=int, default=50, dest="max_pages", help="Maximum pages per domain")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent pages")
    parser.add_argument("--proxy", nargs="*", dest="proxy_urls", help="Proxy URLs to rotate")
    args = parser.parse_args()
    summaries = asyncio.run(run(args.start_urls, args.max_pages, args.concurrency, args.proxy_urls))
    from pprint import pprint
    pprint(summaries)
