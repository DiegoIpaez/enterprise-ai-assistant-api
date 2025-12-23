import re
from datetime import datetime
from logging import Formatter
from pathlib import Path
from typing import ClassVar

BASE_LOG_DIR = Path("./storage/logs")
BASE_LOG_DIR.mkdir(parents=True, exist_ok=True)
DATE = datetime.now().strftime("%Y-%m-%d")


class HttpStatusColorFormatter(Formatter):
    STATUS_COLOR_MAP: ClassVar[dict[str, str]] = {
        "1": "\033[36m",
        "2": "\033[32m",
        "3": "\033[34m",
        "4": "\033[33m",
        "5": "\033[31m",
    }

    LEVEL_COLOR_MAP: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[36m",
        "INFO": "\033[34m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }

    RESET = "\033[0m"

    def format(self, record):
        msg = super().format(record)
        if record.name.startswith("uvicorn.access"):
            match = re.search(r"\s(\d{3})$", msg)
            if match:
                http_code = match.group(1)
                color = self.STATUS_COLOR_MAP.get(http_code[0], self.RESET)
                return f"{color}{msg}{self.RESET}"
        color = self.LEVEL_COLOR_MAP.get(record.levelname, "")
        return f"{color}{msg}{self.RESET}"


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "colored": {
            "()": HttpStatusColorFormatter,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "plain",
            "filename": f"{BASE_LOG_DIR}/{DATE}.log",
            "encoding": "utf-8",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
    "loggers": {
        "uvicorn": {"propagate": True},
        "uvicorn.error": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "fastapi": {"propagate": True},
    },
}
