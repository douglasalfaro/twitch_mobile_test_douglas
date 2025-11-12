# Twitch Mobile UI Automation (Pytest + Selenium)

<p align="center">
  <img src="./demo_run.gif" alt="Demo run" width="420"/>
</p>

> **What this does**
>
> - Opens **m.twitch.tv** in **mobile emulation** (iPhone 12 Pro by default)  
> - Jumps directly to the **Search** view  
> - Searches for a given term (default: **StarCraft II**)  
> - Performs **two distinct scrolls** (visibly separated)  
> - Clicks a result (video/channel), handles popups, tries to start playback  
> - Saves a final screenshot and produces an HTML test report

---

## 🧰 Tech Stack
- **Python 3.11+**
- **Selenium 4**
- **Pytest** (+ `pytest-html` for reporting)
- **webdriver-manager** (auto ChromeDriver setup)
- **Page Object Model (POM)** architecture

---

## 🗂️ Project Structure
```text
twitch_mobile_test_douglas/
├── core/
│   ├── config.py            # Base URL, device name, timeouts, screenshot path
│   ├── driver_setup.py      # Chrome mobile emulation, timeouts, driver init
│   ├── waits.py             # Explicit wait helpers
│   └── logging_setup.py     # Test log configuration
│
├── screens/
│   ├── home_screen.py       # Navigation to search page
│   ├── search_screen.py     # Enter query, scroll twice, open first result
│   └── streamer_screen.py   # Handle popups, start playback, wait for load
│
├── tests/
│   ├── conftest.py          # Pytest fixtures (driver, logging, reporting)
│   └── test_twitch_mobile.py# Main UI test logic
│
├── output/
│   ├── report.html          # Generated test report
│   ├── final_view.png       # Screenshot of final page
│   └── test.log             # Clean log output
│
├── demo_run.gif             # Demo animation of local test
├── requirements.txt         # Dependencies
├── pytest.ini               # Pytest configuration
└── README.md                # Documentation

```

---


## 🧪 How to Run (Windows)

> **Prerequisites**
> - Python **3.11+**
> - Google Chrome installed

### 1️⃣ Create and activate a virtual environment
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2️⃣ Install dependencies
```powershell
pip install -r requirements.txt
```

### 3️⃣ Run tests (generates report + screenshot)
```powershell
pytest
```

## 📦 Artifacts Produced

> - output/report.html	    **Self-contained HTML report
> - output/final_view.png   **Screenshot from the final page
> - output/test.log	    **Clean log output


## ⚙️ Configuration

Edit `core/config.py` as needed:

```python
BASE_URL = "https://m.twitch.tv/"
SEARCH_TERM = "StarCraft II"   # task-required (you may change)
CHANNEL_SLUG = ""              # optional: force a specific channel slug
DEVICE_NAME = "iPhone 12 Pro"  # Chrome mobile emulation device
IMPLICIT_WAIT = 0
PAGELOAD_TIMEOUT = 45
SCREENSHOT_PATH = "output/final_view.png"

```


## ✅ Expected Behavior

- 1️⃣ Opens Twitch mobile site  
- 2️⃣ Searches for the target game/channel  
- 3️⃣ Scrolls twice through results (clearly visible)  
- 4️⃣ Selects and opens a live stream  
- 5️⃣ Waits for playback and takes a screenshot  
- 6️⃣ Generates `output/report.html`


## 📝 Notes & Decisions

> - Mobile emulation via Chrome’s predefined device profiles for deterministic viewport & UA

> - Robust selectors + fallbacks to handle Twitch’s dynamic SPA UI

> - Two-step scroll uses smooth, separated gestures for clear visibility in the GIF

Best-effort stream start (muted autoplay where possible) with popup handling

## 🧾 Run Proof

> - See the embedded demo GIF above

> - After running pytest, open output/report.html for pass/fail and timing details

## 👤 Contact

Douglas Alfaro
📧 douglasalfaro94@gmail.com