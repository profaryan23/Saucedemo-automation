"""
Login test cases for Saucedemo application
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from utils.helpers import SeleniumHelpers


class TestLogin:
    """Test cases for login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        self.driver = webdriver.Chrome()
        self.driver.get(Config.BASE_URL)
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        yield
        self.driver.quit()
    
    def test_valid_login(self):
        """Test login with valid credentials"""
        username_field = (By.ID, "user-name")
        password_field = (By.ID, "password")
        login_button = (By.ID, "login-button")
        
        SeleniumHelpers.send_keys(self.driver, username_field, Config.VALID_USERNAME)
        SeleniumHelpers.send_keys(self.driver, password_field, Config.VALID_PASSWORD)
        SeleniumHelpers.click_element(self.driver, login_button)
        
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
        
        assert "inventory" in self.driver.current_url
    
    def test_invalid_username(self):
        """Test login with invalid username"""
        username_field = (By.ID, "user-name")
        password_field = (By.ID, "password")
        login_button = (By.ID, "login-button")
        
        SeleniumHelpers.send_keys(self.driver, username_field, "invalid_user")
        SeleniumHelpers.send_keys(self.driver, password_field, Config.VALID_PASSWORD)
        SeleniumHelpers.click_element(self.driver, login_button)
        
        error_message = (By.XPATH, "//h3[@data-test='error']")
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located(error_message))
        
        error_text = SeleniumHelpers.get_text(self.driver, error_message)
        assert "do not match" in error_text
    
    def test_invalid_password(self):
        """Test login with invalid password"""
        username_field = (By.ID, "user-name")
        password_field = (By.ID, "password")
        login_button = (By.ID, "login-button")
        
        SeleniumHelpers.send_keys(self.driver, username_field, Config.VALID_USERNAME)
        SeleniumHelpers.send_keys(self.driver, password_field, "wrong_password")
        SeleniumHelpers.click_element(self.driver, login_button)
        
        error_message = (By.XPATH, "//h3[@data-test='error']")
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located(error_message))
        
        error_text = SeleniumHelpers.get_text(self.driver, error_message)
        assert "do not match" in error_text
    
    def test_locked_out_user(self):
        """Test login with locked out user"""
        username_field = (By.ID, "user-name")
        password_field = (By.ID, "password")
        login_button = (By.ID, "login-button")
        
        SeleniumHelpers.send_keys(self.driver, username_field, Config.LOCKED_USERNAME)
        SeleniumHelpers.send_keys(self.driver, password_field, Config.VALID_PASSWORD)
        SeleniumHelpers.click_element(self.driver, login_button)
        
        error_message = (By.XPATH, "//h3[@data-test='error']")
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located(error_message))
        
        error_text = SeleniumHelpers.get_text(self.driver, error_message)
        assert "locked" in error_text.lower()
    
    def test_empty_fields_login(self):
        """Test login with empty username and password"""
        login_button = (By.ID, "login-button")
        
        SeleniumHelpers.click_element(self.driver, login_button)
        
        error_message = (By.XPATH, "//h3[@data-test='error']")
        wait = WebDriverWait(self.driver, Config.EXPLICIT_WAIT)
        wait.until(EC.presence_of_element_located(error_message))
        
        error_text = SeleniumHelpers.get_text(self.driver, error_message)
        assert "required" in error_text.lower()
