import logging

# Logging class to report events to logs File and adapt 
# more features for this project in the future if needed...

class Logging:

    def info(message: str):
        logging.info(message)

    def error(message: str):
        logging.error(message)

    def warning(message: str):
        logging.warning(message)