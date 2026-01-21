import logging
import logging.config

from utils.config import DEBUG


class LoggerManager:
    _initialized = False

    DEFAULT_LOGGER = "ffmpeg-study"

    @classmethod
    def init(cls):
        if cls._initialized:
            return

        config = {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s %(name)s %(levelname)s] %(message)s"
                },
                "console": {
                    "format": f"%(asctime)s %(name)s:%(levelname)s %(filename)s:%(lineno)d %(message)s"
                },
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "default",
                    "filename": "app.log",
                    "encoding": "utf-8",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "ffmpeg-study": {
                    "handlers": ["file", "console"] if DEBUG else "file",
                    'level': 'DEBUG' if DEBUG else 'INFO',
                    "propagate": False,
                }
            },
            "root": {
                "handlers": ["file"],
                "level": "INFO",
            },
        }

        logging.config.dictConfig(config)
        cls._initialized = True

    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        cls.init()
        return logging.getLogger(name or cls.DEFAULT_LOGGER)
