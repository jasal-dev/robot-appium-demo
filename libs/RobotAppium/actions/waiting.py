from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from libs.RobotAppium import context
from libs.RobotAppium.actions.support import Support
from libs.RobotAppium.actions.interactions import Interactions
from libs.RobotAppium.utils.log import Log


class Waiting:

    support = Support()
    log = Log()
    interactions = Interactions()

    GENERIC_TEXT_ELEMENT = {'type': AppiumBy.XPATH,
                            'locator': '//*[@text="::TEXT::" or @label="::TEXT::"]', 
                            'description': 'Element with text ::TEXT::'} 
    GENERIC_TEXT_ELEMENT_CONTAINS = {'type': AppiumBy.XPATH,
                                     'locator': '//*[contains(@text, "::TEXT::") or contains(@label, "::TEXT::") or contains(@value, "::TEXT::")]', 
                                     'description': 'Element containing text ::TEXT::'} 
        
    def wait_for_presence(self, locator: dict, timeout: int = 30):
        """
        Waits until the specified UI element is present in the DOM.

        Args:
            locator (dict): Element locator with keys:
                - 'description' (str): Element description for logging.
                - 'type' (By): Locator type (e.g., AppiumBy.XPATH).
                - 'locator' (str): Locator value.
            timeout (int): Maximum wait time in seconds. Default is 30.

        Returns:
            bool: True if the element becomes present within the timeout.

        Raises:
            AssertionError: If the element does not become present in time.
        """
        wait = WebDriverWait(context.current_application(), timeout)
        logger.info(f"Waiting for element '{locator['description']}' to be present ({locator['locator']})")
        try:
            wait.until(EC.presence_of_element_located((locator['type'], locator['locator'])))
            logger.info("Element found and visible")
            return True
        except Exception as error:
            self.support.capture_screenshot()
            self.support.log_source()
            BuiltIn().fail(f"Element '{locator['description']}' did not became present ({locator['locator']})!\n{error}")
            raise Exception from error

    def wait_for_absence(self, locator: dict, timeout: int = 30):
        """
        Verifies that the specified UI element is not present.

        Waits up to the given timeout to confirm the element does not appear.
        If the element is found, the test fails. If it remains absent, the
        check passes.

        Args:
            locator (dict): Element locator with keys:
                - 'description' (str): Element description for logging.
                - 'type' (By): Locator type (e.g., AppiumBy.XPATH).
                - 'locator' (str): Locator value.
            timeout (int): Maximum wait time in seconds. Default is 30.

        Returns:
            bool: True if the element is not present within the timeout.

        Raises:
            AssertionError: If the element becomes present.
        """
        wait = WebDriverWait(context.current_application(), timeout)
        logger.info(f"Waiting for element '{locator['description']}' to be present ({locator['locator']})")
        try:
            wait.until(EC.presence_of_element_located((locator['type'], locator['locator'])))
            logger.info("Element found and visible")
            raise UnexpectedElementFound()
        except NoSuchElementException as error:
            self.support.capture_screenshot()
            self.support.log_source()
            BuiltIn().fail(f"Element '{locator['description']}' did should not be present ({locator['locator']})!\n{error}")
            raise Exception from error
        except Exception as error:
            logger.info("Element not found")
            return True
        
    def element_with_text_should_be_visible(self, text: str, contains: bool = False):
        """
        Verifies that a UI element with the given text is visible.

        Supports exact or partial text matching.

        Args:
            text (str): Text expected to be visible on the screen.
            contains (bool): If True, matches elements that contain the text.
                If False, matches the text exactly. Default is False.

        Raises:
            AssertionError: If the text is not found or visible.
        """
        self.log.pom_logger(f"Varmistetaan, että teksti {text} on näkyvissä")
        if contains:
            self.wait_for_presence({**self.GENERIC_TEXT_ELEMENT_CONTAINS, 
                                        "locator": self.GENERIC_TEXT_ELEMENT_CONTAINS["locator"].replace("::TEXT::", text),
                                        "description": self.GENERIC_TEXT_ELEMENT_CONTAINS["description"].replace("::TEXT::", text)})
        else:
            self.wait_for_presence({**self.GENERIC_TEXT_ELEMENT, 
                                        "locator": self.GENERIC_TEXT_ELEMENT["locator"].replace("::TEXT::", text),
                                        "description": self.GENERIC_TEXT_ELEMENT["description"].replace("::TEXT::", text)})
            
    def element_with_text_should_not_be_visible(self, text: str, contains: bool = False, timeout: int = 30):
        """
        Verifies that a UI element with the given text is not visible.

        Supports exact or partial text matching when checking for absence.

        Args:
            text (str): Text that should not be visible on the screen.
            contains (bool): If True, checks for elements containing the text.
                If False, checks for an exact text match. Default is False.
            timeout (int): Maximum wait time in seconds. Default is 30.

        Raises:
            AssertionError: If the text is found to be visible.
        """
        self.log.pom_logger(f"Verifying that {text} is not visible")
        if contains:
            self.wait_for_absence({**self.GENERIC_TEXT_ELEMENT_CONTAINS, 
                                   "locator": self.GENERIC_TEXT_ELEMENT_CONTAINS["locator"].replace("::TEXT::", text),
                                   "description": self.GENERIC_TEXT_ELEMENT_CONTAINS["description"].replace("::TEXT::", text)},
                                   timeout=timeout)
        else:
            self.wait_for_absence({**self.GENERIC_TEXT_ELEMENT, 
                                   "locator": self.GENERIC_TEXT_ELEMENT["locator"].replace("::TEXT::", text),
                                   "description": self.GENERIC_TEXT_ELEMENT["description"].replace("::TEXT::", text)},
                                   timeout=timeout)

class UnexpectedElementFound(Exception):
    """Exception raised if element not expected to be found is found"""

    def __init__(self, message="Element should not be present"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message