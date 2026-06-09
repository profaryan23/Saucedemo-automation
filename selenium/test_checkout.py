"""
Checkout test cases for Saucedemo application
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from utils.helpers import SeleniumHelpers


class TestCheckout:
    """Test cases for checkout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        self.driver = webdriver.Chrome()
        self.driver.get(Config.BASE_URL)
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        
        username_field = (By.ID, "user-name")
        password_field = (By.ID, "password")
        login_button = (By.ID, "login-button")
        
        SeleniumHelpers.send_keys(self.driver, username_field, Config.VALID_USERNAME)
        SeleniumHelpers.send_keys(self.driver, password_field, Config.VALID_PASSWORD)
        SeleniumHelpers.click_element(self.driver, login_button)
        
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        add_to_cart_button = (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        SeleniumHelpers.click_element(self.driver, add_to_cart_button)
        
        cart_link = (By.CLASS_NAME, "shopping_cart_link")
        SeleniumHelpers.click_element(self.driver, cart_link)
        
        checkout_button = (By.ID, "checkout")
        SeleniumHelpers.click_element(self.driver, checkout_button)
        
        yield
        self.driver.quit()
    
    def test_checkout_page_loads(self):
        """Test that checkout page loads"""
        first_name_field = (By.ID, "first-name")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(first_name_field)
        )
        
        assert "checkout-step-one" in self.driver.current_url
    
    def test_checkout_without_information(self):
        """Test checkout without filling required fields"""
        continue_button = (By.ID, "continue")
        SeleniumHelpers.click_element(self.driver, continue_button)
        
        error_message = (By.XPATH, "//h3[@data-test='error']")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(error_message)
        )
        
        error_text = SeleniumHelpers.get_text(self.driver, error_message)
        assert "required" in error_text.lower()
    
    def test_complete_checkout(self):
        """Test completing checkout with valid information"""
        first_name = (By.ID, "first-name")
        last_name = (By.ID, "last-name")
        postal_code = (By.ID, "postal-code")
        continue_button = (By.ID, "continue")
        
        SeleniumHelpers.send_keys(self.driver, first_name, "John")
        SeleniumHelpers.send_keys(self.driver, last_name, "Doe")
        SeleniumHelpers.send_keys(self.driver, postal_code, "12345")
        
        SeleniumHelpers.click_element(self.driver, continue_button)
        
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.ID, "finish"))
        )
        
        assert "checkout-step-two" in self.driver.current_url
    
    def test_checkout_overview(self):
        """Test checkout overview page displays order summary"""
        first_name = (By.ID, "first-name")
        last_name = (By.ID, "last-name")
        postal_code = (By.ID, "postal-code")
        continue_button = (By.ID, "continue")
        
        SeleniumHelpers.send_keys(self.driver, first_name, "Jane")
        SeleniumHelpers.send_keys(self.driver, last_name, "Smith")
        SeleniumHelpers.send_keys(self.driver, postal_code, "54321")
        SeleniumHelpers.click_element(self.driver, continue_button)
        
        cart_item = (By.CLASS_NAME, "cart_item")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(cart_item)
        )
        
        items = self.driver.find_elements(*cart_item)
        assert len(items) > 0
    
    def test_finish_order(self):
        """Test completing the order"""
        first_name = (By.ID, "first-name")
        last_name = (By.ID, "last-name")
        postal_code = (By.ID, "postal-code")
        continue_button = (By.ID, "continue")
        
        SeleniumHelpers.send_keys(self.driver, first_name, "Test")
        SeleniumHelpers.send_keys(self.driver, last_name, "User")
        SeleniumHelpers.send_keys(self.driver, postal_code, "00000")
        SeleniumHelpers.click_element(self.driver, continue_button)
        
        finish_button = (By.ID, "finish")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(finish_button)
        )
        SeleniumHelpers.click_element(self.driver, finish_button)
        
        complete_message = (By.CLASS_NAME, "complete-header")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(complete_message)
        )
        
        message_text = SeleniumHelpers.get_text(self.driver, complete_message)
        assert "thank you" in message_text.lower()
