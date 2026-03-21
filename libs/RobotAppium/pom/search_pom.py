from robot.api import logger
from appium.webdriver.common.appiumby import AppiumBy
from libs.RobotAppium.actions.interactions import Interactions
from libs.RobotAppium.actions.waiting import Waiting


class SearchPom:

    interactions = Interactions()
    waiting = Waiting()

    SEARCH_BUTTON = {'type': AppiumBy.ACCESSIBILITY_ID, 
                          'locator': 'Search', 
                          'description': 'Search button on the main screen'}
    SEARCH_INPUT = {'type': AppiumBy.ID, 
                          'locator': 'app.comaps.google:id/query', 
                          'description': 'Search input field'}
    SEARCH_RESULT_ITEM = {'type': AppiumBy.XPATH,
                          'locator': "//android.widget.TextView[@text='::LOCATION::']", 
                          'description': "Search result for '::LOCATION::'"}
    EMPTY_SEARCH_RESULT_MESSAGE = {'type': AppiumBy.XPATH,
                                  'locator': '(//android.widget.LinearLayout[@resource-id="app.comaps.google:id/placeholder"])[2]',
                                  'description': "Message displayed when no search results are found"}


    def search_for_location(self, location_name: str):
        """
        Performs a search for the specified location in the CoMaps app.

        Args:
            location_name (str): The name of the location to search for.
        """
        self.interactions.click_element(self.SEARCH_BUTTON)
        self.interactions.input_text(self.SEARCH_INPUT, location_name)

    def select_location_from_results(self, location_name: str):
        """
        Selects a location from the search results based on the provided location name.

        Args:
            location_name (str): The name of the location to select from the search results.
        """
        self.interactions.click_element({**self.SEARCH_RESULT_ITEM, 
                                         'locator': self.SEARCH_RESULT_ITEM['locator'].replace('::LOCATION::', location_name),
                                         'description': self.SEARCH_RESULT_ITEM['description'].replace('::LOCATION::', location_name)})
        
    def verify_error_message_for_invalid_location(self):
        """
        Verifies that an error message is displayed when a location is not found.
         The actual implementation will depend on the app's UI structure and how error messages are displayed.
         This is a placeholder implementation and should be updated with the correct locator and verification logic.
         """
        self.waiting.wait_for_presence(self.EMPTY_SEARCH_RESULT_MESSAGE, timeout=10)