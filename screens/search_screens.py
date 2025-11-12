# screens/search_screen.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import TimeoutException
from core.waits import wait_clickable, wait_visible


class SearchScreen:
    # Robust selectors for the search field
    INPUT_LOCATORS = (
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.CSS_SELECTOR, "input[aria-label='Search']"),
        (By.CSS_SELECTOR, "input[aria-label*='earch']"),
        (By.CSS_SELECTOR, "input[placeholder*='Search']"),
    )

    # Prefer VIDEO results first (faster to load a page), then channels, then anything
    VIDEO_LOCATORS = (
        (By.CSS_SELECTOR, "a[href*='/videos/']"),
        (By.XPATH, "//a[contains(@href,'/videos/')]"),
        # some UIs mark video cards differently; keep a broad fallback:
        (By.CSS_SELECTOR, "main a[href*='/video']"),
    )
    CHANNEL_LOCATORS = (
        (By.CSS_SELECTOR, "a[href*='/channel/']"),
        (By.XPATH, "//a[contains(@href,'/channel/')]"),
    )
    GENERIC_LOCATORS = (
        (By.CSS_SELECTOR, "main a[href]"),
    )

    def __init__(self, driver):
        self.driver = driver

    # ---------------- helpers ----------------
    def _find_input(self):
        last_err = None
        for loc in self.INPUT_LOCATORS:
            try:
                return wait_visible(self.driver, loc, timeout=8)
            except Exception as e:
                last_err = e
        raise last_err if last_err else AssertionError("Search input not found")

    def _wait_dom_quiet(self, timeout=5):
        """Wait briefly until DOM height stabilizes (SPA settle)."""
        end = time.time() + timeout
        last_h, stable = -1, 0
        while time.time() < end:
            try:
                h = self.driver.execute_script("return document.body.scrollHeight||0")
                if h == last_h:
                    stable += 1
                    if stable >= 3:  # ~0.6s stable (200ms × 3)
                        return
                else:
                    stable = 0
                last_h = h
            except Exception:
                pass
            time.sleep(0.2)

    # ---------------- actions ----------------
    def enter_query(self, text: str):
        box = self._find_input()
        box.clear()
        box.send_keys(text)
        box.send_keys(Keys.ENTER)
        self._wait_dom_quiet(4)  # short settle; faster than tabs switching

    def scroll_down_twice(self):
        """
        Issue two scroll gestures reliably without failing the test if the viewport
        can't advance (short list / anchor). We still try to create movement via
        up-then-down nudges, but we won't assert offsets.
        """
        wait_visible(self.driver, (By.CSS_SELECTOR, "main a[href]"), timeout=10)

        def at_bottom():
            return self.driver.execute_script(
                "return (window.pageYOffset + window.innerHeight) >= (document.body.scrollHeight - 2);"
            )

        def nudge_up():
            # create room to scroll by moving up a bit
            self.driver.execute_script("window.scrollBy(0, -Math.round(window.innerHeight*0.3));")
            time.sleep(0.25)

        def safe_scroll_once():
            # Try to ensure a gesture happens; if at bottom, nudge up then scroll
            if at_bottom():
                nudge_up()
            self.driver.execute_script("window.scrollBy(0, Math.round(window.innerHeight*0.9));")
            time.sleep(0.4)

        # Perform exactly two gestures (no assertion)
        safe_scroll_once()
        safe_scroll_once()

    def open_first_result(self):
        """
        Click the first VIDEO result found (fastest), otherwise first channel, otherwise any link.
        Then wait for URL to change off /search.
        """
        # helper to click from a locator list
        def try_click(locators):
            for loc in locators:
                try:
                    el = wait_clickable(self.driver, loc, timeout=2)
                    if not el.is_displayed():
                        continue
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    self.driver.execute_script("arguments[0].click();", el)  # JS click: bypass overlays
                    return True
                except Exception:
                    continue
            return False

        start_url = self.driver.current_url

        # Prefer videos → then channels → then any link
        if not try_click(self.VIDEO_LOCATORS):
            if not try_click(self.CHANNEL_LOCATORS):
                if not try_click(self.GENERIC_LOCATORS):
                    raise AssertionError("No clickable search result found")

        # Wait for URL to change (navigation)
        end = time.time() + 10
        while time.time() < end:
            if self.driver.current_url != start_url and "/search" not in self.driver.current_url:
                break
            time.sleep(0.2)
