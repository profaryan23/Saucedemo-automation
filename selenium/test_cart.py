class TestCart:
    """Test cases for shopping cart functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new") 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=options)
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
