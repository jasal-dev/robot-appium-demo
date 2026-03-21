from robot.api import logger


class Log:
    def pom_logger(self, message):
        logger.info(f"<b>{message}</b>", html=True)

    def logger(self, message):
        logger.info(f"{message}")

    def debug_logger(self, message):
        logger.info(f"{message}")