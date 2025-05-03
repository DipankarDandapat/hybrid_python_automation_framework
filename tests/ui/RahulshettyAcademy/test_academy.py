import time

import pytest
from selenium.webdriver.common.by import By

from src.pages.RahulshettyAcademyPage.Academy_page import AcademyPage
from src.pages.base_page import BasePage
from src.pages.locators import LoginPageLocators
from src.pages.register_user_page import RegisterUserPage
from src.utils import logger
log = logger.customLogger()

# class TestAcademy:
#
#
#     @pytest.mark.ui
#     def test_academy(self, driver):
#
#         academy_page = AcademyPage(driver)
#         academy_page.open_academyPage_page()
#         time.sleep(3)
#
#         academy_page.clickRadioButtonBaseonName("Radio2")
#
#         time.sleep(5)
#         academy_page.enterandAutoselectCountry("india")
#
#         time.sleep(10)
#


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
