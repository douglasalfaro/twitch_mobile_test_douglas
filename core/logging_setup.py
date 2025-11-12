import logging
from logging import handlers
from pathlib import Path

def setup_logging():
    Path("output").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            handlers.RotatingFileHandler(
                "output/test.log", maxBytes=1_000_000, backupCount=2, encoding="utf-8"
            ),
        ],
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
