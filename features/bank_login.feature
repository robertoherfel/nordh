Feature: Login in XYZ Bank page
  AS a user
  I want to open Chrome browser
  So that I can navigate to XYZ Bank page

  Background:
    Given I open Chrome browser

  @smoke
  Scenario Outline: Login to XYZ Bank as a customer with name <name>
    Given I navigate to XYZ Bank land page
    When I login as "<name>" name
    Then the customer main page is loaded

    Examples:
      | name               | test_id |
      | Harry Potter       | XYZ-001 |
      | Albus Dumbledore   | XYZ-002 |
      | Neville Longbottom | XYZ-003 |
