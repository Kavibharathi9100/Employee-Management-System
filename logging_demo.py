import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
)

# Different log levels
logging.debug("This is a DEBUG message")

logging.info("Application Started Successfully")

logging.warning("Low Disk Space")

logging.error("Database Connection Failed")

logging.critical("Application Crashed")