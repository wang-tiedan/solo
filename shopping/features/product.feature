Feature: Product Management
  As a customer
  I want to add products to my cart and check out
  So that I can purchase my desired products

  Scenario: Add a new product to the cart
    Given I navigate to the add Product to cart
    When I search for the product
    Then the product should be paid successfully
