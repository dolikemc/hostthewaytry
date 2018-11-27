Feature: showing off behave

  Scenario: run a simple test
    Given we have behave installed
    When we implement a test
    When I visit "places:index"
    Then behave will test it for us!