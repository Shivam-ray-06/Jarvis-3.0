from playwright.sync_api import sync_playwright

class BrowserAgent:
    """Agent for browsing the web and extracting content."""
    
    def fetch_page_content(self, url: str) -> str:
        """Navigates to a URL and returns its text content."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, timeout=15000)
                # Extract text content from the body element
                content = page.locator("body").inner_text()
                return content
            except Exception as e:
                return f"Error fetching {url}: {e}"
            finally:
                browser.close()
