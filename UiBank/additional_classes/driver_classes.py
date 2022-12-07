from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class ChromeDriver(webdriver.Chrome):
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        options = webdriver.ChromeOptions()
        prefs = {
            'download.default_directory': '/Users/vladcalomfirescu/Downloads',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        }
        options.add_experimental_option("detach", True)
        options.add_experimental_option('prefs', prefs)
        super().__init__(options=options)


class FirefoxDriver(webdriver.Firefox):
    def __init__(self):
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        super().__init__()


class EdgeDriver(webdriver.Edge):
    def __init__(self):
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        super().__init__()
