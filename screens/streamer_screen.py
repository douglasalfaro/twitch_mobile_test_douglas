# screens/streamer_screen.py
import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from core.waits import wait_visible, wait_clickable

class StreamerScreen:
    PLAYER = (By.CSS_SELECTOR, "video, div[data-a-target='player-overlay-click-handler'], div[data-test-selector='stream-video-player__video']")
    HEADER = (By.CSS_SELECTOR, "header, h1, h2, a[href*='/about']")

    POPUPS = (
        (By.XPATH, "//button[contains(.,'Dismiss') or contains(.,'Not now') or contains(.,'Close')]"),
        (By.XPATH, "//button[contains(.,'Start Watching') or contains(.,'I Understand') or contains(.,'Allow')]"),
        (By.XPATH, "//button[contains(.,'Accept') or contains(.,'Agree') or contains(.,'Only necessary')]"),
        (By.CSS_SELECTOR, "button[aria-label='Close'], button[aria-label*='close']"),
        (By.CSS_SELECTOR, "div[role='dialog'] button"),
    )

    PLAY_OVERLAYS = (
        (By.CSS_SELECTOR, "button[aria-label='Play']"),
        (By.CSS_SELECTOR, "button[data-a-target='player-play-pause-button']"),
        (By.CSS_SELECTOR, "div[data-a-target='player-overlay-click-handler']"),
    )
    UNMUTE = (By.CSS_SELECTOR, "button[aria-label*='mute'], button[aria-label*='Unmute']")

    def __init__(self, driver):
        self.driver = driver

    def dismiss_popups_if_any(self, rounds=2):
        for _ in range(rounds):
            clicked = False
            for loc in self.POPUPS:
                try:
                    el = wait_clickable(self.driver, loc, timeout=1)
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.2)
                    clicked = True
                except Exception:
                    continue
            if not clicked:
                break

    def wait_until_loaded(self, timeout=12):
        try:
            wait_visible(self.driver, self.PLAYER, timeout=timeout)
        except TimeoutException:
            wait_visible(self.driver, self.HEADER, timeout=timeout)

    def _tap_player_center(self):
        try:
            el = wait_visible(self.driver, self.PLAYER, timeout=4)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            # Click center via JS to count as gesture
            self.driver.execute_script("""
                const r = arguments[0].getBoundingClientRect();
                const x = r.left + r.width/2, y = r.top + r.height/2;
                const e = document.elementFromPoint(x, y);
                if (e) e.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
            """, el)
            time.sleep(0.3)
        except Exception:
            pass

    def _press_play_buttons(self):
        for loc in self.PLAY_OVERLAYS:
            try:
                el = wait_clickable(self.driver, loc, timeout=2)
                self.driver.execute_script("arguments[0].click();", el)
                time.sleep(0.3)
                return
            except Exception:
                continue

    def _unmute_if_present(self):
        try:
            el = wait_clickable(self.driver, self.UNMUTE, timeout=1)
            self.driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

    def _js_try_play(self):
        try:
            # Try to find a <video> element and call play()
            played = self.driver.execute_script("""
                const v = document.querySelector('video');
                if (!v) return false;
                const p = v.play ? v.play() : null;
                return true;
            """)
            time.sleep(0.3)
            return played
        except Exception:
            return False

    def _video_playing(self):
        try:
            return self.driver.execute_script("""
                const v = document.querySelector('video');
                if (!v) return false;
                return !v.paused && v.readyState >= 2;
            """)
        except Exception:
            return False

    def try_start_playback(self):
        """
        Best-effort sequence:
        1) Center tap (user gesture)
        2) Press overlay play button
        3) Unmute if needed
        4) Call video.play() via JS
        5) Verify !paused & readyState
        """
        self._tap_player_center()
        self._press_play_buttons()
        self._unmute_if_present()
        self._js_try_play()

        # Give it a moment and verify
        for _ in range(8):
            if self._video_playing():
                return True
            time.sleep(0.4)
        return False
