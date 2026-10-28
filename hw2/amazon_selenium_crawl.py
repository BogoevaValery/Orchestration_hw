#!/home/lerathebest/.local/share/virtualenvs/Orchestration_hw-na0ESBGG/bin/python

import argparse
import json
import random
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError

BASE_URL = "https://www.amazon.com"
MAX_PAGES = 5


def extract_title(card):
    title_el = card.query_selector("h2 a span")
    if title_el:
        return title_el.inner_text().strip()

    title_el = card.query_selector("h2 span")
    if title_el:
        return title_el.inner_text().strip()

    return None


def extract_price(card):
    sec_offer = card.query_selector('[data-cy="secondary-offer-recipe"]')
    if sec_offer:
        price_el = sec_offer.query_selector("span.a-color-base")
        if price_el:
            return price_el.inner_text().strip()

    offscreen = card.query_selector(".a-price .a-offscreen")
    if offscreen:
        return offscreen.inner_text().strip()

    offscreen = card.query_selector(".a-offscreen")
    if offscreen:
        return offscreen.inner_text().strip()

    price_el = card.query_selector("span.a-price")
    if price_el:
        text = price_el.inner_text().strip()
        if text:
            return text

    return None


def scrape_page(page, page_num, query):
    items = []
    try:
        page.wait_for_selector(
            '[data-component-type="s-search-result"]', timeout=30000
        )
    except TimeoutError:
        print(f"Page {page_num} timed out")
        # Сохраняем скриншот и HTML — по ним видно, капча это или что-то ещё
        try:
            Path(f"debug_page_{page_num}.png").write_bytes(page.screenshot())
            Path(f"debug_page_{page_num}.html").write_text(
                page.content(), encoding="utf-8"
            )
            print(f"  Saved debug_page_{page_num}.png / .html")
        except Exception as e:
            print(f"  Failed to save debug info: {e}")
        return items

    cards = page.query_selector_all(
        '[data-component-type="s-search-result"][data-asin]:not([data-asin=""])'
    )
    print(f"Found {len(cards)} cards")

    for card in cards:
        title = extract_title(card)
        price = extract_price(card)

        if title and price:
            items.append({"title": title, "price": price})
        elif title:
            items.append({"title": title, "price": None})

    return items


def main():
    parser = argparse.ArgumentParser(description="Amazon Playwright Crawler")
    parser.add_argument("--query", required=True, help="поисковый запрос")
    args = parser.parse_args()
    query = args.query.strip()
    all_items = []

    with sync_playwright() as p:
        # channel="chrome" — запускаем реальный Google Chrome, а не bundled Chromium.
        # UA и Client Hints будут согласованы с настоящим браузером, поэтому
        # фейковый user_agent не задаём.
        browser = p.chromium.launch(
            headless=True,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            timezone_id="America/New_York",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.amazon.com/",
            },
        )
        # Прячем самые очевидные следы автоматизации до выполнения скриптов страницы
        context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = window.chrome || { runtime: {} };
            """
        )
        page = context.new_page()

        for page_num in range(1, MAX_PAGES + 1):
            print(f"Reading page {page_num}...")
            if page_num == 1:
                url = f"{BASE_URL}/s?k={query.replace(' ', '+')}"
            else:
                url = f"{BASE_URL}/s?k={query.replace(' ', '+')}&page={page_num}"

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except TimeoutError:
                print(f"Timeout while loading {page_num}")
                continue

            # --- диагностика (можно убрать после отладки) ---
            try:
                print("  Final URL:", page.url)
                print("  Title    :", page.title())
                print("  UA       :", page.evaluate("navigator.userAgent"))
                print("  platform :", page.evaluate("navigator.platform"))
                print("  webdriver:", page.evaluate("navigator.webdriver"))
            except Exception as e:
                print(f"  Diagnostics failed: {e}")

            time.sleep(random.uniform(3, 7))

            items = scrape_page(page, page_num, query)
            all_items.extend(items)

        browser.close()

    output_path = Path(f"{query}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)
    print(f"\nTotal: {len(all_items)} thingies; saved to {output_path}")


if __name__ == "__main__":
    main()