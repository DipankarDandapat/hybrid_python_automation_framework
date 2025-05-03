import time

from src.pages.base_page import BasePage
from src.pages.locators import AutomationPracticeLocators
from src.utils import logger



log = logger.customLogger()

from selenium.webdriver.common.keys import Keys
class AcademyPage(BasePage):
    """Login Page class for handling login functionality."""

    def __init__(self, driver):
        """
        Initialize Login Page with WebDriver instance.

        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.locators = AutomationPracticeLocators
        log.info("Initialized AcademyPage")

    def open_academyPage_page(self):
        log.info("Opening AcademyPage page")
        self.open("AutomationPractice",base_url_env_key="RAHULSHETTYACADEMY")
        return self

    def clickRadioButtonBaseonName(self, buttonName):
        if buttonName=="Radio1":
            self.click(self.locators.redioButton1)
        elif buttonName=="Radio2":
            self.click(self.locators.redioButton2)
        else:
            self.click(self.locators.redioButton3)


    def enterandAutoselectCountry(self,country):
        self.input_text(self.locators.autocomplete,country)
        time.sleep(2)

        self.press_key_down("ARROW_DOWN")
        self.press_key_down("ARROW_DOWN")
        time.sleep(1)
        self.press_key_down("ENTER")



