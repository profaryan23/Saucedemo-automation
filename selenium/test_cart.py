"""
Shopping cart test cases for Saucedemo application
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from utils.helpers import SeleniumHelpers


class TestCart:
    """Test cases for shopping cart functionality"""
    
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
        
        yield
        self.driver.quit()
    
    def test_view_cart(self):
        """Test viewing the cart page"""
        cart_link = (By.CLASS_NAME, "shopping_cart_link")
        
        SeleniumHelpers.click_element(self.driver, cart_link)
        
        cart_container = (By.CLASS_NAME, "cart_contents_container")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(cart_container)
        )
        
        assert "cart" in self.driver.current_url
    
    def test_add_multiple_items_to_cart(self):
        """Test adding multiple items to cart"""
        add_to_cart_buttons = (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        
        buttons = self.driver.find_elements(*add_to_cart_buttons)
        for i in range(2):
            buttons[i].click()
        
        cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located(cart_badge))
        
        cart_count = SeleniumHelpers.get_text(self.driver, cart_badge)
        assert cart_count == "2"
    
    def test_cart_item_details(self):
        """Test that cart displays item details correctly"""
        add_to_cart_button = (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        SeleniumHelpers.click_element(self.driver, add_to_cart_button)
        
        cart_link = (By.CLASS_NAME, "shopping_cart_link")
        SeleniumHelpers.click_element(self.driver, cart_link)
        
        cart_item = (By.CLASS_NAME, "cart_item")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(cart_item)
        )
        
        item_name = (By.CLASS_NAME, "inventory_item_name")
        item_price = (By.CLASS_NAME, "inventory_item_price")
        
        assert len(self.driver.find_elements(*item_name)) > 0
        assert len(self.driver.find_elements(*item_price)) > 0
    
    def test_continue_shopping(self):
        """Test continue shopping button"""
        cart_link = (By.CLASS_NAME, "shopping_cart_link")
        SeleniumHelpers.click_element(self.driver, cart_link)
        
        continue_button = (By.ID, "continue-shopping")
        SeleniumHelpers.click_element(self.driver, continue_button)
        
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        assert "inventory" in self.driver.current_url
    
    def test_checkout_button(self):
        """Test checkout button functionality"""
        add_to_cart_button = (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        SeleniumHelpers.click_element(self.driver, add_to_cart_button)
        
        cart_link = (By.CLASS_NAME, "shopping_cart_link")
        SeleniumHelpers.click_element(self.driver, cart_link)
        
        checkout_button = (By.ID, "checkout")
        SeleniumHelpers.click_element(self.driver, checkout_button)
        
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        
        assert "checkout" in self.driver.current_url
