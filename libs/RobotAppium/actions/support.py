import time
from robot.api import logger
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libs.RobotAppium import context

class Support:

    def capture_screenshot(self):
        """
        Captures a screenshot of the current application view and logs it inline.

        Takes a screenshot as a Base64-encoded image and embeds it directly
        into the test log.
        """
        base64_screenshot = context.current_application().get_screenshot_as_base64()
        logger.info(f'</td></tr><tr><td colspan="3">'
                f'<img src="data:image/png;base64, {base64_screenshot}" width="800px">', html=True)
        
    def log_source(self):
        """
        Logs the current page source of the application.

        Retrieves the UI hierarchy (page source) from the active application
        and writes it to the test logs for debugging purposes.
        """
        source = context.current_application().page_source
        logger.info(source)
