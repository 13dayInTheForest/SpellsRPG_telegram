import logging
from logging.config import dictConfig


LOGGING_CONFIG = {
    'disable_existing_loggers': False,
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s]: %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(module)s]: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "detailed",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


def setup_logging():
    # dictConfig(LOGGING_CONFIG)
    pass