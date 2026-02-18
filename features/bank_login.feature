Feature: Login and logout in XYZ Bank page
  AS a user
  I want to open Chrome browser
  So that I can navigate to XYZ Bank page
  And perform login and logout operations

  Background:
    Given I open Chrome browser

  @test_id-<test_id>
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


  @test_id-XYZ-004
  @smoke
  Scenario: Login in XYZ Bank as Harry Potter user and logout
    Given I navigate to XYZ Bank land page
    And I login as "Harry Potter" name
    And the customer main page is loaded
    And I perform logout
    Then I see the XYZ Bank home page

