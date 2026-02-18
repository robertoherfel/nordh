Feature: Bank transactions in XYZ Bank page
  As a user
  I want to open Chrome browser
  So that I can navigate to XYZ Bank page
  And perform transactions like deposits and withdrawals, and verify that the balance is updated accordingly

  Background:
    Given I open Chrome browser

  @test_id-XYZ-005
  @smoke
  Scenario: As Harry Potter user, I deposit 150 Dollars and verify the balance is updated
    Given I navigate to XYZ Bank land page
    And I login as "Harry Potter" name
    And I deposit "100" Dollars
    Then I see the balance updated with "100" Dollars
    And I deposit "50" Dollars
    Then I see the balance updated with "150" Dollars

  @test_id-XYZ-006
  @smoke
  Scenario: As Harry Potter user, I deposit 100 Dollars, I withdrawl 25 Dollars and verify the balance is updated
    Given I navigate to XYZ Bank land page
    And I login as "Albus Dumbledore" name
    And I deposit "100" Dollars
    Then I see the balance updated with "100" Dollars
    And I withdrawl "25" Dollars
    Then I see the balance updated with "75" Dollars

  @test_id-XYZ-007
  @smoke
  Scenario: As Harry Potter user, I check a transaction is recorded after a deposit of 123 Dollars
    Given I navigate to XYZ Bank land page
    And I login as "Albus Dumbledore" name
    And I deposit "123" Dollars
    Then I navigate to the transactions page
    And I see a transaction recorded with "123" Dollars amount
