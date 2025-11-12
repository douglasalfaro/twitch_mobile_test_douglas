![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.x-brightgreen?logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-tested%20✔️-orange?logo=pytest)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Cross--Platform-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Automation](https://img.shields.io/badge/Framework-Page%20Object%20Model-critical)

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

| File | Description |
|------|--------------|
| `output/report.html` | 🧾 **Self-contained HTML test report** |
| `output/final_view.png` | 📸 **Screenshot from the final loaded page** |
| `output/test.log` | 🧹 **Clean log output (test execution details)** |



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

1️⃣ Opens Twitch mobile site  
2️⃣ Searches for the target game/channel  
3️⃣ Scrolls twice through results (clearly visible)  
4️⃣ Selects and opens a live stream  
5️⃣ Waits for playback and takes a screenshot  
6️⃣ Generates `output/report.html`




## 🧾 Run Proof

 - See the embedded demo GIF above

 - After running pytest, open output/report.html for pass/fail and timing details

## 🧠 Design Decisions

- **Page Object Model (POM) Architecture:**  
  Each screen (Home, Search, Streamer) is isolated as a class, encapsulating selectors and actions.  
  This design minimizes coupling and allows scalable test extension for new flows.

- **Resilient Synchronization:**  
  Custom wait helpers (`wait_visible`, `wait_clickable`) replace arbitrary sleeps, ensuring stable runs under dynamic Twitch SPA behavior.

- **Smart Scrolling Logic:**  
  Uses measured offset tracking and fallback recovery to handle lazy-loading or fixed-height views.  
  It scrolls intelligently rather than relying on pixel guesses.

- **Environment Independence:**  
  `webdriver-manager` automatically provisions ChromeDriver and manages versioning — no manual setup needed.  
  The config file (`core/config.py`) centralizes device type, timeouts, and URLs, making the suite portable across machines and CI.

- **Self-contained Reporting:**  
  `pytest-html` produces a single HTML artifact with embedded screenshots for easy CI/CD integration and traceability.

- **Scalable Extensibility:**  
  The structure supports adding more modules (e.g., Login, Chat, Following) without touching core test logic.  
  Test data and environment config can easily be externalized (e.g., JSON, YAML, or environment variables).

- **Error Resilience:**  
  StreamerScreen methods use best-effort recovery (popup dismissal, retry playback) rather than hard failures.

---

## 🚀 Senior-Level Engineering

- Architected for **growth and maintainability** (can scale to multiple Twitch features).  
- **Automates a live, asynchronous, SPA-based mobile site** — complex real-world use case.  
- Implements **clean abstractions**, **fault tolerance**, and **CI-ready reporting**.  
- Reflects a **professional QA automation standard** seen in enterprise-level frameworks.

## 👤 Contact

Douglas Alfaro
📧 douglasalfaro94@gmail.com