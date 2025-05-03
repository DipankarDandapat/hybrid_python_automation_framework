"""
Page Locators Module.

This module contains all UI element locators used in page objects.
Locators are organized by page for easy maintenance.
"""
from selenium.webdriver.common.by import By


class RegisterUserPageLocators:
    """Register Page Locators."""

    signup_Name = (By.XPATH, "//input[@placeholder='Name']")
    signup_Email = (By.XPATH, "//input[@data-qa='signup-email']")
    signup_Button= (By.XPATH, "//button[normalize-space()='Signup']")
    #user_title=    (By.XPATH, "//input[@type='radio']")
    user_title=    (By.XPATH, "//div[@class='radio-inline']")
    address=    (By.XPATH, "//input[@id='address1']")





class LoginPageLocators:
    """Login Page Locators."""
    
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberMe")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")


class DashboardPageLocators:
    """Dashboard Page Locators."""
    
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".welcome-message")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    PROFILE_DROPDOWN = (By.ID, "profile-dropdown")
    SETTINGS_LINK = (By.ID, "settings-link")
    NOTIFICATION_ICON = (By.ID, "notification-icon")
    NOTIFICATION_COUNT = (By.CSS_SELECTOR, ".notification-count")
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.ID, "search-button")
    MENU_ITEMS = (By.CSS_SELECTOR, ".menu-item")
    USER_AVATAR = (By.CSS_SELECTOR, ".user-avatar")



class AutomationPracticeLocators:
    redioButton1 = (By.XPATH, "//input[@value='radio1']")
    redioButton2 = (By.XPATH, "//input[@value='radio2']")
    redioButton3 = (By.XPATH, "//input[@value='radio3']")
    autocomplete = (By.XPATH, "//input[@id='autocomplete']")