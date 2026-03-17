from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def amazon_scraper_price(link):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        if not link.startswith(("http://", "https://")):
            link = f"https://{link}"

        page.goto(link, wait_until="domcontentloaded")

        try:
            page.get_by_role("button", name="Continuar comprando").click(timeout=3000)
        except PlaywrightTimeoutError:
            pass

        price_box = page.locator("span.a-price").first
        
        if price_box is None:
            raise ValueError("Price not found")

        whole = price_box.locator("span.a-price-whole").inner_text().strip()
        fraction = price_box.locator("span.a-price-fraction").inner_text().strip()

        whole = whole.replace(",", "").replace("\n", "").strip()
        
        price = f"{whole},{fraction}"
        
        scraped_name = page.locator("span.a-size-large.product-title-word-break").inner_text().strip()
        
        if scraped_name is None:
            raise ValueError('Name not found')
        
        browser.close()
        return price, scraped_name

