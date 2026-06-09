"""
Helper functions for automation testing
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SeleniumHelpers:
    """Common selenium helper methods"""
    
    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        """Wait for an element to be present in DOM"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=10):
        """Wait for an element to be visible"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=10):
        """Wait for an element to be clickable"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    @staticmethod
    def click_element(driver, locator, timeout=10):
        """Wait for element to be clickable and click it"""
        element = SeleniumHelpers.wait_for_element_clickable(driver, locator, timeout)
        element.click()
    
    @staticmethod
    def send_keys(driver, locator, text, timeout=10):
        """Wait for element to be visible and send keys"""
        element = SeleniumHelpers.wait_for_element_visible(driver, locator, timeout)
        element.clear()
        element.send_keys(text)
    
    @staticmethod
    def get_text(driver, locator, timeout=10):
        """Wait for element to be visible and get its text"""
        element = SeleniumHelpers.wait_for_element_visible(driver, locator, timeout)
        return element.text
