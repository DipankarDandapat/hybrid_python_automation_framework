import time

import pytest
from selenium.webdriver.common.by import By

from src.pages.RahulshettyAcademyPage.Academy_page import AcademyPage
from src.pages.base_page import BasePage
from src.pages.locators import LoginPageLocators
from src.pages.register_user_page import RegisterUserPage
from src.utils import logger
log = logger.customLogger()

class TestAcademy:


    @pytest.mark.ui
    def test_academy_radio_button(self, driver):

        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.clickRadioButtonBaseonName("Radio2")


    @pytest.mark.ui
    def test_academy_select_country(self, driver):
        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.enterandAutoselectCountry("india")


    @pytest.mark.ui
    def test_academy_select_dropdown(self, driver):
        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.selectDropdownByValue("option3")


    @pytest.mark.ui
    def test_academy_select_checkBox(self, driver):
        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.selectCheckBox()


    @pytest.mark.ui
    def test_academy_switch_windows(self, driver):
        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.switchWindows()


    @pytest.mark.ui
    def test_academy_open_tab(self, driver):
        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.switchOpenTab()


    @pytest.mark.ui
    def test_academy_open_alert(self, driver):
        academy_page = AcademyPage(driver)
        academy_page.open_academyPage_page()
        academy_page.switchAlert("dipankar")


