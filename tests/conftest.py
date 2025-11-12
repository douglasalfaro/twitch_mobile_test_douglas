import os
import time
import pytest
from datetime import datetime
from pathlib import Path

from core import config
from core.driver_setup import create_mobile_driver
from core.logging_setup import setup_logging

# Initialize logging once per session
def pytest_sessionstart(session):
    setup_logging()

@pytest.fixture
def driver():
    drv = create_mobile_driver(config.DEVICE_NAME)
    yield drv
    drv.quit()

# Record test outcome so we can take screenshots on failure
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only act on actual test-call phase failures (not setup/teardown)
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is None:
            return

        # Ensure folder
        shots_dir = Path("output") / "failures"
        shots_dir.mkdir(parents=True, exist_ok=True)

        # Build filename: testname_timestamp.png
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = report.nodeid.replace("::", "__").replace("/", "_").replace("\\", "_")
        shot_path = shots_dir / f"{safe_name}_{timestamp}.png"

        try:
            drv.save_screenshot(str(shot_path))
            # Try to attach to pytest-html if available
            try:
                from pytest_html import extras
                if hasattr(report, "extra"):
                    report.extra.append(extras.image(str(shot_path)))
            except Exception:
                # Attachment failed? it's fine; the file is still saved.
                pass
        except Exception:
            pass
