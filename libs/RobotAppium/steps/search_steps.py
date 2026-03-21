from robot.api.deco import keyword
from libs.RobotAppium import context
from libs.RobotAppium.actions.device import Device
from libs.RobotAppium.actions.waiting import Waiting
from libs.RobotAppium.actions.interactions import Interactions
from libs.RobotAppium.pom.search_pom import SearchPom


class search_steps:

    interactions = Interactions()
    search = SearchPom()


    @keyword('I search for target location "${location}"')
    def search_for_target_location(self, location):
        """
        Searches for a target location in the CoMaps app.

        Args:
            location (str): The name of the location to search for.
        """
        self.search.search_for_location(location)

    @keyword('I should see an error message indicating that the location was not found')
    def should_see_error_message_for_invalid_location(self):
        """
        Verifies that an error message is displayed when a location is not found.
        """
        # This is a placeholder implementation. The actual locator and interaction logic will depend on the app's UI structure.
        self.search.verify_error_message_for_invalid_location()
 