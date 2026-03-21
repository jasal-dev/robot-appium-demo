from robot.api.deco import keyword
from libs.RobotAppium import context
from libs.RobotAppium.actions.device import Device
from libs.RobotAppium.actions.waiting import Waiting

class main_steps:

    device = Device()
    waiting = Waiting()
    
    @keyword("I am on the CoMaps main screen")
    def open_app(self):
        """
        Opens the CoMaps app and verifies that the main screen is displayed.

        This step initializes the app session using the Device action, then waits for a key element
        on the main screen to be visible to confirm successful navigation.

        Expected behavior:
            - The app is launched successfully.
            - The main screen is displayed, indicated by the presence of a specific UI element (e.g., a unique button or label).
        """
        self.device.open_app(app_package='app.comaps.google', app_activity='app.organicmaps.DownloadResourcesActivity')

    @keyword('I restart the app')
    def restart_app(self):
        """
        Restarts the CoMaps app.
        """
        self.device.restart_application()
        
        