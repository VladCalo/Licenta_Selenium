from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from UiBank import constants as const


class Products:

    def __init__(self, driver: WebDriver, product_type):
        self.product_type = product_type
        self.driver = driver
        self.products = {
            "Loans": 1,
            "Credit Cards": 2,
            "Mobile Banking": 3
        }
        self.driver.implicitly_wait(15)

    def go_to_product(self):
        self.driver.find_element(By.ID, 'navbarDropdown').click()
        self.driver.find_element(
            By.XPATH,
            f'/html/body/app-root/body/app-nav-menu/header/nav/div/div/ul/li[2]/div/a[{self.products[self.product_type]}]'
        ).click()
