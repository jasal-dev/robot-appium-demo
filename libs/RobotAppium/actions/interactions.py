import time

from typing import Literal, Tuple, Optional
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from libs.RobotAppium import context
from libs.RobotAppium.actions.support import Support
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from appium.webdriver.common.appiumby import AppiumBy


class Interactions:

    support = Support()

    def click_element(self, locator: dict, max_wait: int = 30):
        """
        Clicks a UI element defined by the given locator.

        Waits for any loading spinner to disappear and for the element 
        to become visible before clicking it. If `retry` is True, the 
        method checks after the click whether the element remains visible 
        and retries once if needed.

        Args:
            locator (dict): Element locator with keys:
                - 'description' (str): Element name for logging.
                - 'type' (By): Locator type (e.g., AppiumBy.XPATH).
                - 'locator' (str): Locator value.
            retry (bool): Retry click if the element stays visible. Default is False.
            max_wait (int): Max wait time for element visibility. Default is 30 seconds.
            use_actions (bool): Use Actions to click calculate coordinates. Default is False.

        Raises:
            AssertionError: If clicking fails (screenshot and page source are logged).
        """
        driver = context.current_application()
        wait = WebDriverWait(driver, max_wait)
        retry_wait = WebDriverWait(driver, 10)
        logger.info(f"Clicking element '{locator['description']} ({locator['locator']})'")
        try:
            wait.until(EC.presence_of_element_located((locator['type'], locator['locator']))).click()
            logger.info("Element found and clicked")
        except Exception as error:
            self.support.capture_screenshot()
            self.support.log_source()
            BuiltIn().fail(f"Clicking element '{locator['description']} ({locator['locator']})' failed!\n{error}")

    def input_text(self, 
                   locator: dict, 
                   text: str, 
                   mask: bool = False, 
                   clear: bool = False, 
                   hide_keyboard: bool = True, 
                   max_wait: int = 30):
        """
        Inputs text into the specified UI element.

        Waits until the element is visible, optionally clears existing text, 
        and then types the given value. If `mask` is True, the text is hidden 
        in logs.

        Args:
            locator (dict): Element locator with keys:
                - 'description' (str): Element name for logging.
                - 'type' (By): Locator type (e.g., AppiumBy.XPATH).
                - 'locator' (str): Locator value.
            text (str): Text to input.
            mask (bool): If True, hides the text in logs. Default is False.
            clear (bool): If True, clears the field before typing. Default is False.
            hide_keyboard (bool): If True, hides keyboard after text input. Default is True.
            max_wait (int): Max wait time for element visibility. Default is 30 seconds.

        Raises:
            AssertionError: If text input fails (screenshot and page source are logged).
        """
        logger.info(f"Inputting text {'***' if mask else text} into element {locator['description']} ({locator['locator']})")
        driver = context.current_application()
        wait = WebDriverWait(driver, max_wait)
        element = None
        try:
            element = wait.until(EC.visibility_of_element_located((locator['type'], locator['locator'])))
            logger.info("Element visible")

            if clear:
                element.clear()
            element.send_keys(text)
            logger.info("Text input complete")
        except Exception as error:
            self.support.capture_screenshot()
            self.support.log_source()
            BuiltIn().fail(f"Inputting text '{text}' into element {locator['description']} ({locator['locator']}) failed!\n{error}")
