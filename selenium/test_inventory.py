"""
Inventory test cases for Saucedemo application
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from utils.helpers import SeleniumHelpers


class TestInventory:
    """Test cases for inventory/products page"""
    
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
    
    def test_inventory_page_loads(self):
        """Test that inventory page loads with products"""
        inventory_items = (By.CLASS_NAME, "inventory_item")
        items = self.driver.find_elements(*inventory_items)
        
        assert len(items) > 0
    
    def test_product_display(self):
        """Test that products display correctly"""
        product_name = (By.CLASS_NAME, "inventory_item_name")
        product_price = (By.CLASS_NAME, "inventory_item_price")
        
        names = self.driver.find_elements(*product_name)
        prices = self.driver.find_elements(*product_price)
        
        assert len(names) > 0
        assert len(prices) > 0
        assert len(names) == len(prices)
    
    def test_add_product_to_cart(self):
        """Test adding a product to cart"""
        add_to_cart_button = (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        
        SeleniumHelpers.click_element(self.driver, add_to_cart_button)
        
        cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located(cart_badge))
        
        cart_count = SeleniumHelpers.get_text(self.driver, cart_badge)
        assert cart_count == "1"
    
    def test_remove_product_from_cart(self):
        """Test removing a product from cart"""
        add_to_cart_button = (By.XPATH, "//button[contains(text(), 'Add to cart')]")
        
        SeleniumHelpers.click_element(self.driver, add_to_cart_button)
        
        remove_button = (By.XPATH, "//button[contains(text(), 'Remove')]")
        WebDriverWait(self.driver, Config.EXPLICIT_WAIT).until(
            EC.presence_of_element_located(remove_button)
        )
        SeleniumHelpers.click_element(self.driver, remove_button)
        
        cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        assert len(self.driver.find_elements(*cart_badge)) == 0
