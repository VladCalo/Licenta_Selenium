from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from UiBank import constants as const
from UiBank.uibank import *


# TODO: Continue CreditCard methods. UiBank Credit Cards section under maintenance!

class CreditCard:

    def __init__(self, driver: WebDriver):
        uibank = UiBank()
        self.location = uibank.select_product('Credit Cards')
        self.driver = driver
        self.card_type = {
            'Travel': 2,
            'Cash Back': 3,
            'Treat': 4,
        }
        self.driver.implicitly_wait(15)

    def select_card_type(self, card):
        self.location()
        self.driver.find_element(
            By.XPATH,
            f'/html/body/app-root/body/div/app-credit-cards/div[{self.card_type[card]}]/div[3]/div'
        ).click()

    def travel_card(self):
        self.select_card_type('Travel')
        # TODO: ...

    def cash_back_card(self):
        self.select_card_type('Cash Back')
        # TODO: ...

    def treat_card(self):
        self.select_card_type('Treat')
        # TODO: ...
