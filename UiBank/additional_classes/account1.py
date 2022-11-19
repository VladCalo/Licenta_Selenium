from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from Task1.UiBank import constants as const
from Task1.UiBank.uibank import *


class Account:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.accounts_box = self.driver.find_element(
            By.XPATH,
            '/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[2]'
        )
        self.nr_of_accounts = len(self.accounts_box.find_elements(By.XPATH, '*'))
        self.driver.implicitly_wait(15)

    def select_random_account(self):
        account_elem = self.driver.find_element(
            By.XPATH,
            f'/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[2]/div[{random.randint(1, self.nr_of_accounts)}]/div/div/div/div[1]/a'
        )
        account_elem.click()

    def select_account_by_name(self, account_name):
        for i in range(1, self.nr_of_accounts + 1):
            account_elem = self.driver.find_element(
                By.XPATH,
                f'/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[2]/div[{i}]/div/div/div/div[1]/a'
            )
            name = account_elem.text
            if name == account_name:
                account_elem.click()
                break

    def dispute_transaction(self):
        self.select_random_account()
        self.driver.find_element(By.ID, 'disputeTransaction').click()