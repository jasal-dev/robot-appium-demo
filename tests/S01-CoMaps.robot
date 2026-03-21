*** Settings ***
Library            ${CURDIR}/../libs/RobotAppium/steps/main_steps.py
Library            ${CURDIR}/../libs/RobotAppium/steps/search_steps.py
Library            ${CURDIR}/../libs/RobotAppium/steps/bookmark_steps.py


*** Variables ***




*** Test Cases ***
S01 CoMaps - TEST 01: Creating and deleting bookmark collections
    [Documentation]    Verify that creating and deleting bookmark collections works correctly
    [Tags]    CoMaps    Bookmarks
    Given I am on the CoMaps main screen
      And I navigate to the bookmarks/routes import screen
    When I create a new bookmark collection named "Test Collection"
    Then I should see the bookmark collection "Test Collection" in the list
    When I delete the bookmark collection named "Test Collection"
    Then I should not see the bookmark collection "Test Collection" in the list

    [Teardown]  I restart the app

S01 CoMaps - TEST 02: Importing bookmarks and routes - valid file
    [Documentation]    Verify that importing bookmarks and routes from a valid file works correctly
    [Tags]    CoMaps    Bookmarks    Import
    Given I am on the CoMaps main screen
      And I navigate to the bookmarks/routes import screen
      And I have a bookmarks/routes file "bookmarks_routes_valid.gpx"
    When I import the bookmarks/routes file
    Then I should see the bookmark collection "My Exported Collection" in the list

    [Teardown]  Run Keywords  
    ...    I delete file "bookmarks_routes_valid.gpx" from device
    ...    I restart the app

S01 CoMaps - TEST 03: Importing bookmarks and routes - invalid file
    [Documentation]    Verify that importing bookmarks and routes from an invalid file shows an error message
    [Tags]    CoMaps    Bookmarks    Import
    Given I am on the CoMaps main screen
      And I navigate to the bookmarks/routes import screen
      And I have a bookmarks/routes file "bookmarks_routes_invalid.gpx"
    When I import the bookmarks/routes file
    Then I should see an error message indicating the file is invalid

    [Teardown]  Run Keywords
    ...    I delete file "bookmarks_routes_invalid.gpx" from device
    ...    I restart the app

S01 CoMaps - TEST 04: Invalid location search
    [Documentation]    Verify that searching for an invalid location shows an appropriate error message
    [Tags]    CoMaps    Search
    Given I am on the CoMaps main screen
    When I search for target location "InvalidLocation123"
    Then I should see an error message indicating that the location was not found

    [Teardown]  I restart the app

S01 CoMaps - TEST 05: Special characters in bookmark collections
    [Documentation]    Verify that creating and deleting bookmark collections with special characters works correctly
    [Tags]    CoMaps    Bookmarks
    Given I am on the CoMaps main screen
      And I navigate to the bookmarks/routes import screen
    When I create a new bookmark collection named "Test Collection !@#$%^&*()å"
    Then I should see the bookmark collection "Test Collection !@#$%^&*()å" in the list

    [Teardown]  I restart the app