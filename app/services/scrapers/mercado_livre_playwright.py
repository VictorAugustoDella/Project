from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def ml_scraper_price(link):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        if not link.startswith(("http://", "https://")):
            link = f"https://{link}"

        page.goto(link, wait_until="domcontentloaded")

        price = page.locator('meta[itemprop="price"]').get_attribute("content")

        if price is None:
            raise ValueError("Price not found")

        price = price.replace(".", ",")
        
        scraped_name = page.locator("span.ui-pdp-title").inner_text().strip()
        
        if scraped_name is None:
            raise ValueError('Name not found')
        
        browser.close()
        return price, scraped_name