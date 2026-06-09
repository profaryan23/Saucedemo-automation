"""
Configuration file for Saucedemo automation tests
"""

class Config:
    """Base configuration class"""
    
    # Application URLs
    BASE_URL = "https://www.saucedemo.com"
    
    # Browser configurations
    BROWSER = "chrome"
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    
    # Test users
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    LOCKED_USERNAME = "locked_out_user"
    PROBLEM_USERNAME = "problem_user"
    
    # Database configurations
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "password"
    DB_NAME = "saucedemo"
    DB_PORT = 3306
