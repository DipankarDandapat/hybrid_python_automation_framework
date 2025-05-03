import time

import pytest
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.pages.locators import LoginPageLocators
from src.pages.register_user_page import RegisterUserPage
from src.utils import logger
log = logger.customLogger()

class TestRegister:
    """Test class for Register functionality."""

    @pytest.mark.ui
    def test_register(self, driver):


        register_user = RegisterUserPage(driver)
        register_user.open(url_path="login")

        register_user.enterName("deep")
        register_user.enterEmail("d1@gmail.com")
        register_user.clickSignupButton()
        time.sleep(5)
        register_user.clickUserTitle("Mr.")
        time.sleep(5)
        register_user.scrollToAdress()
        time.sleep(5)



    # @pytest.mark.ui
    # def test_login_with_valid_credentials(self, driver):
    #     """
    #     Test login with valid credentials.
    #
    #     Args:
    #         driver: WebDriver fixture
    #     """
        # Initialize base page
        # base_page = BasePage(driver)
        
        # Open login page
        # base_page.open("login")
        #
        # # Enter credentials and login
        # base_page.input_text(LoginPageLocators.USERNAME_INPUT, "testuser")
        # base_page.input_text(LoginPageLocators.PASSWORD_INPUT, "password123")
        # base_page.click(LoginPageLocators.LOGIN_BUTTON)
        #
        # # Take screenshot
        # base_page.take_screenshot("login_success.png")
        #
        # log.info("Login with valid credentials test completed")

    # @pytest.mark.ui
    # def test_login_with_invalid_credentials(self, driver):
    #     """
    #     Test login with invalid credentials.
    #
    #     Args:
    #         driver: WebDriver fixture
    #     """
    #     # Initialize base page
    #     base_page = BasePage(driver)
        
        # Open login page
        # base_page.open("login")
        #
        # # Enter invalid credentials and login
        # base_page.input_text(LoginPageLocators.USERNAME_INPUT, "invaliduser")
        # base_page.input_text(LoginPageLocators.PASSWORD_INPUT, "invalidpassword")
        # base_page.click(LoginPageLocators.LOGIN_BUTTON)
        #
        # # Verify error message is displayed
        # assert base_page.is_element_present(LoginPageLocators.ERROR_MESSAGE), "Error message not displayed"
        #
        # # Take screenshot
        # base_page.take_screenshot("login_failure.png")
        #
        # log.info("Login with invalid credentials test completed")
