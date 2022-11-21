import os
import string
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from . import constants as const
from Task1.UiBank.additional_classes.main_page_navbar import MainPageNavbar
from Task1.UiBank.additional_classes.products import Products
import random
import json
import re
import shutil
import time

from .additional_classes.account import Account, RandomAccount, AccountByName
from .additional_classes.credit_card import CreditCard


class UiBank(webdriver.Chrome):
    def __init__(self, driver_path=r'/usr/local/bin', teardown=False):
        self.teardown = teardown
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        super(UiBank, self).__init__(options=options)

        self.loans = []
        self.accounts = []
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def landing_page_and_login(self):
        self.get(const.BASE_URL)
        self.find_element(By.ID, 'username').send_keys(const.username)
        self.find_element(By.ID, 'password').send_keys(const.password)
        self.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        ).click()

    def apply_for_new_account(self, account_type='savings'):
        self.navigate_to('Accounts')
        self.find_element(
            By.XPATH,
            '/html/body/app-root/body/div/app-accounts/div/div[1]/div/div[1]/div[2]'
        ).click()

        def get_random_string(length):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for _ in range(length))
            return result_str

        accountName = get_random_string(3) + " Account"
        accountNickname = self.find_element(By.ID, 'accountNickname')
        accountNickname.send_keys(accountName)
        self.find_element(
            By.CSS_SELECTOR,
            f'option[value={account_type}]'
        ).click()
        self.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        ).click()

        account = {
            "accountId": self.find_element(By.ID, 'accountId').text,
            "accountName": accountName,
            "account_type": account_type,
            "balance": "$100"
        }
        self.accounts.append(account)

        file_path = os.getcwd() + '/UiBank/outputs/bot_generated_accounts.txt'
        with open(file_path, 'a') as output_file:
            if os.stat(file_path).st_size != 0:
                output_file.write(",")
                output_file.write('\n')
            output_file.write(json.dumps(account))

    def navigate_to(self, where_to='Accounts'):
        navbar = MainPageNavbar(driver=self, where_to=where_to)
        navbar.go_to_nav_item()

    def select_product(self, product_type='Loans'):
        product = Products(driver=self, product_type=product_type)
        product.go_to_product()

    def get_help(self):
        self.navigate_to(where_to='Help')
        self.find_element(By.ID, 'fullName').send_keys(const.fullName)
        self.find_element(By.ID, 'emailAddress').send_keys(const.email)
        message_field = self.find_element(By.ID, 'message')
        message_field.clear()
        message_field.send_keys(const.help_message)

        contact_us_button = self.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        )
        # contact_us_button.click()

    def apply_for_loan(self):
        self.select_product()
        self.find_element(By.ID, 'applyButton').click()
        self.find_element(By.ID, 'email').send_keys(const.email)
        self.find_element(By.ID, 'amount').send_keys(str(const.loan_amount))

        self.find_element(By.ID, 'term').click()
        random_nr = random.randint(0, 3)
        self.find_element(
            By.CSS_SELECTOR,
            f'option[value="{str(const.loan_term[random_nr])}"]'
        ).click()

        self.find_element(By.ID, 'income').send_keys(str(const.yearly_income))
        self.find_element(By.ID, 'age').send_keys(str(const.age))
        self.find_element(By.ID, 'submitButton').click()

        loan_id = self.find_element(By.ID, 'loanID').text
        rate = self.find_element(By.ID, 'rate').text

        loan = {'loan_id': loan_id, 'rate': rate, 'applicant_age': const.age, 'term': const.loan_term[random_nr],
                'loan_amount': const.loan_amount, 'yearly_income': const.yearly_income}
        self.loans.append(loan)

        file_path = os.getcwd() + '/UiBank/outputs/loans.txt'
        with open(file_path, 'a') as output_file:
            if os.stat(file_path).st_size != 0:
                output_file.write(",")
                output_file.write('\n')
            output_file.write(json.dumps(loan))

    def already_have_loan(self):  # , which_loan=0):
        self.select_product()
        self.find_element(By.ID, 'existingButton').click()

        loan_id_field = self.find_element(By.ID, 'quoteID')
        loan_id_field.send_keys(self.loans[random.randint(0, len(self.loans) - 1)]['loan_id'])

        self.find_element(
            By.CSS_SELECTOR,
            'button[type="submit"]'
        ).click()

    # TODO: create_credit_card()
    def create_credit_card(self):
        card = CreditCard(driver=self)
        # card.method()

    def transfer_funds(self):
        self.get(const.main_page)
        self.navigate_to()
        # self.find_element(
        #     By.XPATH,
        #     '/html/body/app-root/body/div/app-accounts/div/div[2]/div/div[2]/div[1]/div[2]/a'
        # ).click()
        self.find_element(
            By.LINK_TEXT,
            'Transfer Funds'
        ).click()

        fromAccount = self.find_element(By.ID, 'fromAccount')
        fromAccount.click()
        fromAccount_children = fromAccount.find_elements(By.CSS_SELECTOR, '*')
        fromAccount_selection = fromAccount_children[random.randint(0, len(fromAccount_children) - 1)]
        fromAccount_selection.click()
        account_name_id = fromAccount_selection.text
        available_amount = re.findall(r'[$][0-9]+', account_name_id)[0]
        available_amount = available_amount[1:]

        toAccount = self.find_element(By.ID, 'toAccount')
        toAccount_children = toAccount.find_elements(By.CSS_SELECTOR, '*')
        toAccount_children[random.randint(0, len(toAccount_children) - 1)].click()

        self.find_element(By.ID, 'amountTransferred').send_keys(round(random.uniform(1, float(available_amount))))

        self.find_element(
            By.XPATH,
            '/html/body/app-root/body/div/app-transfer-money/div[1]/div[2]/form/button'
        ).click()

        self.find_element(
            By.XPATH,
            '//*[@id="exampleModal"]/div/div/div[3]/button[2]'
        ).click()

    def automate_dispute_center_random_account(self):
        self.get(const.main_page)
        self.navigate_to('Accounts')
        random_account = RandomAccount(driver=self)
        random_account.go_to_dispute_center()
        random_account.go_to_current_disputes()
        random_account.go_to_closed_disputes()
        random_account.dispute_new_transaction()

    def automate_dispute_center_by_account_name(self, account_name):
        self.navigate_to('Accounts')
        account_by_name = AccountByName(driver=self, account_name=account_name)
        account_by_name.go_to_dispute_center()
        account_by_name.go_to_current_disputes()
        account_by_name.go_to_closed_disputes()
        account_by_name.dispute_new_transaction()

    # TODO: download_button not clickable
    def download_transactions_random_account(self):
        self.navigate_to('Accounts')
        random_account = RandomAccount(driver=self)
        random_account.download_transactions()

    # TODO: download_button not clickable
    def download_transactions_by_account_name(self, account_name):
        self.navigate_to('Accounts')
        account_by_name = AccountByName(driver=self, account_name=account_name)
        account_by_name.download_transactions()
