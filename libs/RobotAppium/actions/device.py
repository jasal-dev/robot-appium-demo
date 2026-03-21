import time
import base64
import os

from robot.api import logger
from appium import webdriver
from appium.options.common import AppiumOptions
from libs.RobotAppium import context


class Device:

    def open_app(self, **kwargs):
        """
        Starts the CoMapsApp Android app session (local Appium + emulator) and registers it in the context cache.

        Creates a new driver session only if there is no current cached application. Builds
        Appium capabilities from `kwargs`, connects to the local Appium server, and registers
        the driver under the alias 'CoMapsApp'.

        Expected kwargs:
            appium_server_url (str): Appium server URL. Defaults to http://127.0.0.1:4723.
            app (str): Path to app file (.apk/.aab). Optional if appPackage/appActivity is provided.
            app_package (str): Android app package name.
            app_activity (str): Android app activity name.
            device_name (str): Emulator/device name (optional, defaults to Android Emulator).
            os_version (str): Android platform version (optional).

        Returns:
            Any: The registered application handle from `context._cache.register(...)` (alias 'CoMapsApp').
        """
        logger.info("Launching the app")
        if not context._cache.current:
            logger.info("Creating a new session")
            context.currently_logged_in_user = None
            appium_options = {
                'appium:automationName': 'UIAutomator2',
                'platformName': 'android',
                'appium:alias': 'CoMapsApp',
                #'appium:noReset': True,
                'appium:fullReset': False,
                'appium:fastReset': True,
                'appium:locale': 'GB',
                'appium:maxTypingFrequency': 20,
                'appium:settings[waitForIdleTimeout]': 600,
                'appium:settings[waitForSelectorTimeout]': 300,
                'appium:deviceName': kwargs.get('device_name', 'Android Emulator'),
                'appium:language': 'en',
                'appium:autoGrantPermissions': 'true'
            }

            if kwargs.get('app'):
                appium_options['appium:app'] = kwargs['app']

            if kwargs.get('app_package'):
                appium_options['appium:appPackage'] = kwargs['app_package']

            if kwargs.get('app_activity'):
                appium_options['appium:appActivity'] = kwargs['app_activity']

            if kwargs.get('os_version'):
                appium_options['appium:platformVersion'] = kwargs['os_version']

            logger.info(f"DEBUG: Appium capabilities: {appium_options}")

            desired_caps = AppiumOptions().load_capabilities(caps=appium_options)
            appium_server_url = kwargs.get('appium_server_url', 'http://127.0.0.1:4723')
            application = webdriver.Remote(appium_server_url, options=desired_caps)

            return context._cache.register(application, 'CoMapsApp')

    def restart_application(self, reset: bool = False, app_bundle: str = "app.comaps.google"):
        """
        Restarts the Android application.

        Terminates the app, optionally clears application data, and then
        relaunches it.

        Args:
            reset (bool): If True, clears the application data while restarting.
        """        
        driver = context.current_application()
        logger.info("Closing the app")
        driver.terminate_app(app_bundle)
        time.sleep(3)
        if reset:
            logger.info("Clearing app data")
            driver.execute_script("mobile: clearApp", {'appId': app_bundle})

        logger.info("Launching the app")
        driver.activate_app(app_bundle)
        driver.orientation = "PORTRAIT"
        # TODO: Wait for app to be visible

    def upload_file_to_device(self, source_file_path: str, target_device_path: str = None):
        """
        Uploads a local file to the Android device using Appium.

        Args:
            source_file_path (str): Absolute or relative path to the local file.
            target_device_path (str): Optional target absolute path on the device.
                If not provided, defaults to /sdcard/Download/<source filename>.

        Raises:
            FileNotFoundError: If the source file does not exist.
            ValueError: If source_file_path is empty.
        """
        if not source_file_path or not source_file_path.strip():
            raise ValueError("source_file_path is required")

        normalized_source_path = os.path.abspath(source_file_path)

        if not os.path.isfile(normalized_source_path):
            raise FileNotFoundError(f"File not found: {normalized_source_path}")

        if target_device_path and target_device_path.strip():
            resolved_target_device_path = target_device_path.strip()
        else:
            file_name = os.path.basename(normalized_source_path)
            resolved_target_device_path = f"/sdcard/Download/uploaded/{file_name}"

        with open(normalized_source_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("utf-8")

        driver = context.current_application()
        logger.info(f"Uploading file '{normalized_source_path}' to '{resolved_target_device_path}'")
        driver.push_file(resolved_target_device_path, encoded_content)
        logger.info("File upload completed")

    def delete_file_from_device(self, device_file_path: str, fail_if_missing: bool = False):
        """
        Deletes a file from the Android device using Appium.

        Args:
            device_file_path (str): Absolute path of the file on the device.
            fail_if_missing (bool): If True, fails when the file does not exist.
                If False (default), missing files are ignored.

        Raises:
            ValueError: If device_file_path is empty.
            RuntimeError: If the delete command fails.
        """
        if not device_file_path or not device_file_path.strip():
            raise ValueError("device_file_path is required")

        resolved_device_file_path = device_file_path.strip()
        remove_args = [resolved_device_file_path] if fail_if_missing else ["-f", resolved_device_file_path]

        driver = context.current_application()
        logger.info(f"Deleting file from device: '{resolved_device_file_path}'")
        command_result = driver.execute_script(
            "mobile: shell",
            {
                "command": "rm",
                "args": remove_args
            }
        )

        if isinstance(command_result, dict):
            stderr_output = command_result.get("stderr", "")
            exit_code = command_result.get("code", 0)
            if exit_code not in (0, None):
                raise RuntimeError(f"Failed to delete file '{resolved_device_file_path}': {stderr_output or command_result}")

        logger.info("File delete completed")
