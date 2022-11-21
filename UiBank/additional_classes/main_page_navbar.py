from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from Task1.UiBank import constants as const
# from Task1.UiBank.uibank import UiBank


class MainPageNavbar:

    def __init__(self, driver: WebDriver, where_to):
        self.where_to = where_to
        self.driver = driver
        self.nav_item = {
            'Accounts': 1,
            'Help': 3,
            'Profile': 4,
            'Logout': 5
        }
        self.driver.implicitly_wait(15)

    def go_to_nav_item(self):
        # uibank = UiBank()
        # uibank.main_page()
        self.driver.find_element(
            By.XPATH,
            f'/html/body/app-root/body/app-nav-menu/header/nav/div/div/ul/li[{self.nav_item[self.where_to]}]/a'
        ).click()
