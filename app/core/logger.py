import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",

    handlers=[
        RotatingFileHandler(
            "logs/hrms.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
    ),
        logging.StreamHandler()
    ]
)

# Create logger
logger = logging.getLogger("HRMS")