# Created by danielfrid at 5/25/2025
Feature: Registered users can set up an search agent
  # Enter feature description here

  Scenario: Registered user can click on "create search agent"
    When I am a registered user with email address
    And I am in the search menu
    Then I can click on the "create search button"
    And it looks clickable

  Scenario: created search agent is persisted
    When A search agent was created via the button
    Then the search agent is persisted and active

  Scenario: Active search agent sends an email
    When A new search result is appears
    And search agent is active
    And Search agents are being refereshed
    Then the user associated with a search agent receives an Email