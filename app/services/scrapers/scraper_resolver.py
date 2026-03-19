from urllib.parse import urlparse
from app.exceptions import ValidationError
from app.services.scrapers.amazon_playwright import amazon_scraper_price
from app.services.scrapers.mercado_livre_playwright import ml_scraper_price


def get_scraper(url: str):
    if "://" not in url:
        url = f"https://{url}"

    hostname = urlparse(url).hostname

    if not hostname:
        raise ValidationError("Invalid url")

    hostname = hostname.lower()

    if hostname == "amazon.com.br" or hostname.endswith(".amazon.com.br"):
        return amazon_scraper_price, "amazon"

    if hostname == "mercadolivre.com.br" or hostname.endswith(".mercadolivre.com.br"):
        return ml_scraper_price, "mercadolivre"

    raise ValidationError("link must be a amazon or mercadolivre link")
