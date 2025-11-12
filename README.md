# Twitch Mobile UI Automation (Pytest + Selenium)

<p align="center">
  <img src="./demo_run.gif" alt="Demo run" width="600"/>
</p>


> **What this does**  
> - Opens **m.twitch.tv** in **mobile emulation** (iPhone 12 Pro by default)  
> - Jumps directly to the **Search** view  
> - Searches for a given term (default: **StarCraft II**)  
> - Performs **two distinct scrolls** (visibly separated)  
> - Clicks a result (video/channel), handles popups, tries to start playback  
> - Saves a final screenshot and produces an HTML test report

---

## Tech Stack

- **Python 3.11**
- **Selenium 4**
- **Pytest** (+ `pytest-html` reporting)
- **webdriver-manager** (auto ChromeDriver)
- **Page Object Model (POM)** layout

---

## Project Structure

├── core/
│ ├── config.py # Tweak base URL, device name, timeouts, screenshot path
│ ├── driver_setup.py # Chrome mobile emulation, global timeouts
│ ├── waits.py # Explicit wait helpers
│ └── logging_setup.py # Clean test logs in output/test.log
├── screens/
│ ├── home_screen.py # Navigation to search page
│ ├── search_screen.py # Enter query, double-scroll, open first result
│ └── streamer_screen.py # Dismiss popups, wait for stream, best-effort play
├── tests/
│ ├── conftest.py # Pytest fixtures (driver, logging, reporting)
│ └── test_twitch_mobile.py
├── output/ # report.html, screenshots, logs (created on run)
├── requirements.txt
├── pytest.ini # HTML report + CLI logging defaults
└── demo_run.gif # Short demo of the local run


---

## How to Run (Windows)

> Prereqs: Python 3.11+, Google Chrome installed.

```powershell
# 1) Create and activate venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Run tests (generates report.html + screenshot)
pytest


Artifacts produced

report.html (self-contained HTML report)

output/final_view.png (screenshot from the final page)

output/test.log (clean test log)


Configuration

Edit core/config.py:

BASE_URL = "https://m.twitch.tv/"
SEARCH_TERM = "StarCraft II"   # required by the task (adjust if needed)
CHANNEL_SLUG = ""              # optional: force a channel slug
DEVICE_NAME = "iPhone 12 Pro"  # Chrome mobile emulation device
IMPLICIT_WAIT = 0
PAGELOAD_TIMEOUT = 45
SCREENSHOT_PATH = "output/final_view.png"


Notes & Decisions

Mobile emulation via Chrome’s predefined device profiles (consistent viewport & UA).

Robust selectors + fallbacks to handle Twitch’s dynamic/Spa UI.

Two-step scroll uses smooth, separated gestures for clear visibility in the GIF.

Best-effort stream start (muted autoplay where possible) with popup handling.


Run Proof

See the embedded demo GIF above.

After pytest, open report.html for pass/fail and timing details.

Contact

Douglas Alfaro
Email: douglasalfaro94@gmail.com