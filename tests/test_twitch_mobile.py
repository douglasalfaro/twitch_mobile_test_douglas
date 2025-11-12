import os
import pytest
from core import config
from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.streamer_screen import StreamerScreen  # used after navigation

def test_search_and_capture(driver):
    # 1) Open home
    home = HomeScreen(driver)
    home.open(config.BASE_URL)

    # 2) Go to search
    home.tap_search_icon()

    # 3) Enter query
    search = SearchScreen(driver)
    search.enter_query(config.SEARCH_TERM)

    # 4) Scroll twice (verified)
    search.scroll_down_twice()

    # 5) Open first channel/result and verify we left /search
    start_url = driver.current_url
    search.open_first_result()
    final_url = driver.current_url
    assert final_url != start_url and "/search" not in final_url, f"Expected to leave search page, got: {final_url}"

    # 6) Handle popups, wait for load, and try to start playback (best-effort)
    stream = StreamerScreen(driver)
    stream.dismiss_popups_if_any()
    stream.wait_until_loaded()
    stream.try_start_playback()

    # 7) Screenshot evidence
    os.makedirs(os.path.dirname(config.SCREENSHOT_PATH), exist_ok=True)
    driver.save_screenshot(config.SCREENSHOT_PATH)
    print(f"\nScreenshot saved to: {config.SCREENSHOT_PATH}\n")
    assert os.path.exists(config.SCREENSHOT_PATH) and os.path.getsize(config.SCREENSHOT_PATH) > 0
