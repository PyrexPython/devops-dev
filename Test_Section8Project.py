Python 3.13.0 (v3.13.0:60403a5409f, Oct  7 2024, 00:37:40) [Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> import pytest
... from flask import Flask
... from unittest.mock import patch
... from your_module import HomeFinder  # Replace with the actual module name of your code
... 
... # Test the HomeFinder class
... @patch('your_module.requests.get')  # Mocking requests.get
... def test_get_housing_commissions(mock_get):
...     # Mock the response object
...     mock_response = mock_get.return_value
...     mock_response.status_code = 200
...     mock_response.content = '<div class="housing-commission">Commission 1</div>'
...     
...     # Create an instance of HomeFinder
...     finder = HomeFinder()
... 
...     # Call the method and assert the result
...     commissions = finder.get_housing_commissions('NY')
...     assert len(commissions) == 1
...     assert commissions[0] == 'Commission 1'
... 
... @patch('your_module.requests.get')
... def test_search_homes(mock_get):
...     # Mock the response object
...     mock_response = mock_get.return_value
...     mock_response.status_code = 200
...     mock_response.content = '''
...         <div class="property-listing">
...             <h2 class="property-address">123 Main St</h2>
...             <span class="property-price">$1200</span>
...             <span class="property-beds">2</span>
...             <span class="property-baths">1</span>
...         </div>
...     '''
...     
...     # Create an instance of HomeFinder
    finder = HomeFinder()

    # Call the method and assert the result
    homes = finder.search_homes('NY', 'New York', '10001', 'apartment', 'available')
    assert len(homes) == 1
    assert homes[0]['address'] == '123 Main St'
    assert homes[0]['price'] == '$1200'
    assert homes[0]['bedrooms'] == '2'
    assert homes[0]['bathrooms'] == '1'
