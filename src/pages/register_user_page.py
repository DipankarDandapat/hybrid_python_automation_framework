from src.pages.base_page import BasePage
from src.pages.locators import RegisterUserPageLocators
from src.utils import logger
log = logger.customLogger()


class RegisterUserPage(BasePage):
    """Login Page class for handling login functionality."""

    def __init__(self, driver):
        """
        Initialize Login Page with WebDriver instance.

        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.locators = RegisterUserPageLocators
        log.info("Initialized RegisterUserPageLocators")



    def enterName(self,Name):
        self.input_text(self.locators.signup_Name,Name)

    def enterEmail(self,Email):
        self.input_text(self.locators.signup_Email,Email)

    def clickSignupButton(self):
        self.click(self.locators.signup_Button)


    def clickUserTitle(self,title):
        self.find_all_elements_click_based_on_text(self.locators.user_title,title)

    def scrollToAdress(self):
        self.scroll_to_element_automatic(self.locators.address)