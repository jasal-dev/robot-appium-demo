from robot.api.deco import keyword
from libs.RobotAppium import context
from libs.RobotAppium.actions.device import Device
from libs.RobotAppium.actions.waiting import Waiting
from libs.RobotAppium.actions.interactions import Interactions
from libs.RobotAppium.pom.bookmarks_pom import BookmarksPom


class bookmark_steps:

    interactions = Interactions()
    bookmarks = BookmarksPom()
    device = Device()


    @keyword('I navigate to the bookmarks/routes import screen')
    def navigate_to_bookmarks_routes_import_screen(self):
        """
        Navigates to the bookmarks/routes import screen in the CoMaps app.
        """
        self.bookmarks.navigate_to_bookmarks()

    @keyword('I have a bookmarks/routes file "${file_path}"')
    def upload_bookmarks_routes_file(self, file_path):
        """
        Uploads a bookmarks/routes file to the device
        Args:
            file_path (str): The path to the bookmarks/routes file to upload.
        """
        self.bookmarks.upload_bookmarks_routes_file(f"./data/{file_path}")

    @keyword('I import the bookmarks/routes file')
    def import_bookmarks_routes_file(self):
        """
        Clicks the "Import Favourites" button to import the bookmarks/routes file in the CoMaps app.
        """
        self.bookmarks.import_bookmarks_routes_file('bookmarks_routes_valid.gpx')

    @keyword('I should see the bookmark collection "${collection_name}" in the list')
    def verify_bookmarks_routes_imported(self, collection_name):
        """
        Verifies that the bookmarks and routes from the imported file are displayed in the app.
        """
        self.bookmarks.verify_bookmarks_routes_imported(collection_name)

    @keyword('I should see an error message indicating the file is invalid')
    def verify_import_error_visible(self):
        """
        Verifies that an error message is displayed indicating that the imported file is invalid.
        """
        self.bookmarks.import_error_visible()

    @keyword('I delete file "${file_name}" from device')
    def delete_file_from_device(self, file_name):
        """
        Deletes a file from the device.
        Args:
            file_name (str): The name of the file to delete.
        """
        self.device.delete_file_from_device(f"/sdcard/Download/uploaded/{file_name}")

    @keyword('I create a new bookmark collection named "${collection_name}"')
    def create_bookmark_collection(self, collection_name):
        """
        Creates a new bookmark collection with the specified name.
        Args:
            collection_name (str): The name of the bookmark collection to create.
        """
        self.bookmarks.create_bookmark_collection(collection_name)

    @keyword('I delete the bookmark collection named "${collection_name}"')
    def delete_bookmark_collection(self, collection_name):
        """
        Deletes a bookmark collection with the specified name.
        Args:
            collection_name (str): The name of the bookmark collection to delete.
        """
        self.bookmarks.delete_bookmark_collection(collection_name)

    @keyword('I should not see the bookmark collection "${collection_name}" in the list')
    def verify_bookmark_collection_not_visible(self, collection_name):
        """
        Verifies that a bookmark collection with the specified name is not visible in the list.
        Args:
            collection_name (str): The name of the bookmark collection to check.
        """
        self.bookmarks.verify_bookmark_collection_not_visible(collection_name)
