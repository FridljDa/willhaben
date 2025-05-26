# Created by danielfrid at 5/25/2025
Feature: Filtering search results
  # Enter feature description here

  Scenario: Expand advanced search
    When I am in the basic search view
    And I click on "advanced search"
    Then Advanced search menu is expanded

  Scenario: Collapse advanced search
    When I am in the advanced search view
    And I click on "close advanced search"
    Then Advanced search is collapsed

  Scenario: Date filter lower bound
    When I am in the advanced search view
    And I select a lower bound for a date filter
    Then the table is filtered for values above

  Scenario: Date filter upper bound
    When I am in the advanced search view
    And I select an upper bound for a date filter
    Then the table is filtered for values below

  #Scenario: Numeric filter
  #  When

  #Scenario: String filter
