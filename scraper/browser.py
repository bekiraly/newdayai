from playwright.sync_api import sync_playwright
from typing import Callable, Any, Dict


def with_browser(fn: Callable[[Any], Any]) -> Any:
    """
    Playwright browser'ı aç-kapat; fn(page) şeklinde callback çalıştır.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            result = fn(page)
        finally:
            browser.close()
        return result


def fetch_html(url: str, wait_selector: str | None = None) -> str:
    """
    Basit: URL'ye git -> HTML'i döndür.
    """
    def _runner(page):
        page.goto(url, wait_until="networkidle")
        if wait_selector:
            page.wait_for_selector(wait_selector, timeout=8000)
        return page.content()

    return with_browser(_runner)


def search_in_site(url: str, query: str, search_selector: str, result_click_selector: str) -> str:
    """
    Sitede arama çubuğunu bulup takım/maç arayan generic fonksiyon.
    'search_selector' -> input,
    'result_click_selector' -> ilk sonuç
    """
    def _runner(page):
        page.goto(url, wait_until="networkidle")
        page.fill(search_selector, query)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        page.wait_for_selector(result_click_selector, timeout=8000)
        page.click(result_click_selector)
        page.wait_for_timeout(2000)
        return page.content()

    return with_browser(_runner)
