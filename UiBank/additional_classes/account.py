from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from UiBank import constants as const
from UiBank.uibank import *
from abc import ABC, abstractmethod
import os
from pathlib import Path


class Account(ABC):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.accounts_box = self.driver.find_element(
            By.XPATH,
            '/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[2]'
        )
        self.nr_of_accounts = len(self.accounts_box.find_elements(By.XPATH, '*'))
        self.driver.implicitly_wait(15)

    @abstractmethod
    def select_account(self):
        pass

    def go_to_dispute_center(self):
        nr = self.select_account()
        self.driver.find_element(
            By.ID,
            'disputeTransaction'
        ).click()
        self.driver.find_element(
            By.ID,
            'accountSelection'
        ).click()
        self.driver.find_element(
            By.XPATH,
            f'//*[@id="accountSelection"]/option[{nr}]'
        ).click()
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        ).click()

    def go_to_current_disputes(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button[data-target="#collapseOne"]'
        ).click()

    def go_to_closed_disputes(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button[data-target="#collapseTwo"]'
        )

    # TODO: unable to check the box
    def dispute_new_transaction(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button[data-target="#collapseThree"]'
        ).click()
        transactionsTable = self.driver.find_element(
            By.XPATH,
            '//*[@id="collapseThree"]/div/div[3]/table[2]/tbody'
        )
        transactions = transactionsTable.find_elements(By.TAG_NAME, 'tr')
        nrTransactions = len(transactions)
        print(nrTransactions)
        if nrTransactions == 0:
            print('Account has no transactions')
            return
        else:
            # for i in range(random.randint(1, nrTransactions)):
            #     self.driver.find_element(
            #         By.XPATH,
            #         f'//*[@id="mat-checkbox-{str(33 + i)}"]/label/div'
            #     ).click()
            checkbox = self.driver.find_element(
                By.ID,
                'mat-checkbox-26'
            )
            checkbox.click()

            self.driver.find_element(
                By.XPATH,
                '//*[@id="collapseThree"]/div/div[2]/div'
            ).click()

    # TODO: download_button not clickable
    def download_transactions(self):
        nr = self.select_account()
        # self.driver.find_element(By.ID, 'downloadTransactions').click()
        self.driver.find_element(By.XPATH, '//*[@id="downloadTransactions"]').click()

        source = str(os.path.join(Path.home(), "Downloads"))
        destination = os.getcwd() + '/UiBank/outputs/transactions/'
        allfiles = os.listdir(source)

        for f in allfiles:
            if 'transactionData' in str(f):
                src_path = os.path.join(source, f)
                dst_path = os.path.join(destination, f)
                os.rename(src_path, dst_path)


class RandomAccount(Account):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def select_account(self):
        random_nr = random.randint(0, self.nr_of_accounts)
        account_elem = self.driver.find_element(
            By.XPATH,
            f'/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[2]/div[{random_nr}]/div/div/div/div[1]/a'
        )
        account_elem.click()
        return random_nr

    def dispute_new_transaction(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            'button[data-target="#collapseThree"]'
        )
        transactionsTable = self.driver.find_element(
            By.XPATH,
            '//*[@id="collapseThree"]/div/div[3]/table[2]/tbody'
        )
        transactions = transactionsTable.find_elements(By.CSS_SELECTOR, '*')
        nrTransactions = len(transactions)
        if nrTransactions == 0:
            print('Account has no transactions')
            return
        else:
            # nrDisputeTransactions = random.randint(1, nrTransactions)
            for i in range(random.randint(1, nrTransactions)):
                self.driver.find_element(
                    By.XPATH,
                    f'//*[@id="mat-checkbox-{str(33 + i)}"]/label/div'
                ).click()
            self.driver.find_element(
                By.XPATH,
                '//*[@id="collapseThree"]/div/div[2]/div'
            ).click()


class AccountByName(Account):
    def __init__(self, driver: WebDriver, account_name):
        self.account_name = account_name
        super().__init__(driver)

    def select_account(self):
        for i in range(1, self.nr_of_accounts + 1):
            account_elem = self.driver.find_element(
                By.XPATH,
                f'/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[2]/div[{i}]/div/div/div/div[1]/a'
            )
            name = account_elem.text
            if name == self.account_name:
                account_elem.click()
                return i
