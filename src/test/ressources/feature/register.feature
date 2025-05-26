# Created by danielfrid at 5/25/2025
Feature: Unregistered user can register
  # Enter feature description here

  Scenario: Unregistered user can register
    When I am an unregistered user
    Then I can register using social register