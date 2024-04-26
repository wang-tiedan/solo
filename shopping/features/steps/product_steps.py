from behave import given, when, then, fixture, use_fixture
import os
import sys
import django
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Set up the Django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
sys.path.append('D:/project/solo')  # Add the project root directory to sys.path
django.setup()

@fixture
def django_test_case(context):
    """Setup a Django test case and provide a live_server_url."""
    context.test_case = LiveServerTestCase()
    context.test_case.setUpClass()
    context.live_server_url = context.test_case.live_server_url
    yield context.test_case
    context.test_case.tearDownClass()

def before_all(context):
    """Setup the environment before all tests, initializing the browser instance."""
    use_fixture(django_test_case, context)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    context.browser = webdriver.Chrome(executable_path='path/to/chromedriver', options=options)
    context.browser.implicitly_wait(5)

def after_all(context):
    """Close the browser after all tests are completed."""
    context.browser.quit()

@given(u'I navigate to the add Product to cart')
def step_impl(context):
    # Use Django url name
    cart_url = context.live_server_url + reverse('view_cart')
    context.browser.get(cart_url)
    assert "Shopping Cart" in context.browser.title

@when(u'I search for the product')
def step_impl(context):
    # Form to search for a product
    search_input = context.browser.find_element(By.NAME, 'query')
    search_input.send_keys('Test Product')
    search_button = context.browser.find_element(By.CSS_SELECTOR, 'form[action="{% url \'product-detail\' %}"] button')
    search_button.click()

@then(u'the product should be payed successfully')
def step_impl(context):
    # Check for a success message or the number of items in the cart
    success_message = context.browser.find_element(By.CSS_SELECTOR, 'div.success').text
    assert 'Product has been added' in success_message
