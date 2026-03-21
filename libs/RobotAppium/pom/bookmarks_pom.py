from robot.api import logger
from appium.webdriver.common.appiumby import AppiumBy
from libs.RobotAppium.actions.interactions import Interactions
from libs.RobotAppium.actions.device import Device
from libs.RobotAppium.actions.waiting import Waiting


class BookmarksPom:

    interactions = Interactions()
    waiting = Waiting()
    device = Device()

    PLACES_BUTTON = {'type': AppiumBy.ACCESSIBILITY_ID, 
                          'locator': 'Places', 
                          'description': 'Places button on the main screen'}
    IMPORT_FAVORITES_BUTTON = {'type': AppiumBy.XPATH, 
                          'locator': '//android.widget.TextView[@resource-id="app.comaps.google:id/text" and @text="Import Favourites"]', 
                          'description': 'Import Favourites button'}
    DOWNLOADS_FOLDER = {'type': AppiumBy.XPATH,
                          'locator': '//android.widget.TextView[@resource-id="android:id/title" and @text="Download"]', 
                          'description': "Downloads folder"}
    UPLOADED_FOLDER = {'type': AppiumBy.XPATH,
                          'locator': '//android.widget.TextView[@resource-id="android:id/title" and @text="uploaded"]', 
                          'description': "Uploaded folder"}
    ROUTES_FILE = {'type': AppiumBy.XPATH,
                          'locator': '//android.widget.FrameLayout[@content-desc="Preview the file ::FILE::"]', 
                          'description': "Bookmarks/routes file ::FILE::"}
    USE_THIS_FOLDER = {'type': AppiumBy.ID,
                          'locator': 'android:id/button1', 
                          'description': "Use this folder button"}
    ALLOW_BUTTON = {'type': AppiumBy.XPATH,
                          'locator': '//android.widget.Button[@resource-id="android:id/button1" and @text="ALLOW"]',
                            'description': "Allow button"}
    CREATE_NEW_LIST_BUTTON = {'type': AppiumBy.XPATH,
                              'locator': '//android.widget.TextView[@resource-id="app.comaps.google:id/text" and @text="Create a new list"]',
                              'description': "Create new list button"}
    NEW_LIST_NAME_INPUT = {'type': AppiumBy.ID,
                              'locator': 'app.comaps.google:id/et__input',
                              'description': "New list name input field"}
    ACCEPT_LIST_NAME_BUTTON = {'type': AppiumBy.ID,
                              'locator': 'android:id/button1',
                              'description': "Accept list name button"}
    LIST_OPTIONS_BUTTON = {'type': AppiumBy.XPATH,
                           'locator': '//android.widget.TextView[@resource-id="app.comaps.google:id/name" and @text="::COLLECTION_NAME::"]/following-sibling::android.widget.ImageView[1]',
                           'description': "Options button for bookmark collection ::COLLECTION_NAME::"}
    DELETE_LIST_BUTTON = {'type': AppiumBy.XPATH,
                           'locator': '//android.widget.TextView[@resource-id="app.comaps.google:id/bottom_sheet_menu_item_text" and @text="Delete"]',
                           'description': "Delete bookmark collection button"}




    def navigate_to_bookmarks(self):
        """
        Navigates to the bookmarks screen
        """
        self.interactions.click_element(self.PLACES_BUTTON)

    def upload_bookmarks_routes_file(self, file_path: str):
        """
        Uploads a bookmarks/routes file to the device.

        Args:
            file_path (str): The path to the bookmarks/routes file to upload.
        """
        self.device.upload_file_to_device(file_path)

    def import_bookmarks_routes_file(self, file_name: str):
        """
        Clicks the "Import Favourites" button, navigates to the downloads folder, and selects the specified bookmarks/routes file.

        Args:
            file_name (str): The name of the bookmarks/routes file to import (e.g., 'bookmarks_routes_valid.gpx').
        """
        self.interactions.click_element(self.IMPORT_FAVORITES_BUTTON)
        try:
            self.interactions.click_element(self.DOWNLOADS_FOLDER, max_wait=5)
            self.interactions.click_element(self.UPLOADED_FOLDER, max_wait=5)
        except Exception:
            # We are likely already in the uploaded folder, so we can ignore this error and continue
            self.interactions.click_element(self.USE_THIS_FOLDER)  
        self.interactions.click_element(self.ALLOW_BUTTON)

    def verify_bookmarks_routes_imported(self, bookmark_name: str):
        """
        Verifies that the bookmarks and routes from the imported file are displayed in the app.

        Args:
            bookmark_name (str): The name of a bookmark or route that should be visible after import (e.g., 'My Places').
        """
        self.waiting.element_with_text_should_be_visible(bookmark_name)

    def import_error_visible(self):
        """
        Checks if an error message is visible on the screen.

        """
        self.waiting.element_with_text_should_be_visible('Failed to load Favourites. The file may be corrupted or defective.')

    def create_bookmark_collection(self, collection_name: str):
        """
        Creates a new bookmark collection with the specified name.

        Args:
            collection_name (str): The name of the bookmark collection to create.
        """
        self.interactions.click_element(self.CREATE_NEW_LIST_BUTTON)
        self.interactions.input_text(self.NEW_LIST_NAME_INPUT, collection_name)
        self.interactions.click_element(self.ACCEPT_LIST_NAME_BUTTON)

    def delete_bookmark_collection(self, collection_name: str):
        """
        Deletes a bookmark collection with the specified name.

        Args:
             collection_name (str): The name of the bookmark collection to delete.
        """
        self.interactions.click_element({**self.LIST_OPTIONS_BUTTON, 
                                         'locator': self.LIST_OPTIONS_BUTTON['locator'].replace('::COLLECTION_NAME::', collection_name),
                                         'description': self.LIST_OPTIONS_BUTTON['description'].replace('::COLLECTION_NAME::', collection_name)})
        self.interactions.click_element(self.DELETE_LIST_BUTTON)

    def verify_bookmark_collection_not_visible(self, collection_name: str):
        """
        Verifies that a bookmark collection with the specified name is not visible in the list.

        Args:
            collection_name (str): The name of the bookmark collection that should not be visible.
        """
        self.waiting.element_with_text_should_not_be_visible(collection_name, timeout=5)