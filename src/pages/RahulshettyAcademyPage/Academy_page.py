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
        self.open("RAHULSHETTYACADEMY",url_path="AutomationPractice")
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
        self.press_key("ARROW_DOWN")
        self.press_key("ARROW_DOWN")
        self.press_key("ENTER")


    def selectDropdownByValue(self,dropdownvalue):
        self.select_dropdown_option_by_value(locator=self.locators.dropdown,value=dropdownvalue)


    def selectCheckBox(self):
        if not self.is_element_selected(self.locators.option1checkbox):
            self.click(self.locators.option1checkbox)


    def switchWindows(self):
        self.click(self.locators.switchWindows)
        # l=self.get_window_handles()
        # self.switch_to_window_by_handle(l[1])
        self.switch_to_window_by_index(1)
        self.click(self.locators.logo)
        self.close_current_window_and_switch_back()

    def switchOpenTab(self):
        self.click(self.locators.opentab)
        self.switch_to_window_by_index(1)
        self.click(self.locators.logo)
        self.open_new_tab_and_switch()
        self.close_current_window_and_switch_back()

    def switchAlert(self,name):
        self.input_text(self.locators.alertName,name)
        self.click(self.locators.alertButton)
        time.sleep(3)
        print(self.wait_for_alert())
        print("#######################")
        self.accept_alert()
        time.sleep(3)


