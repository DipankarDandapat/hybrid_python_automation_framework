"""
WebDriver Module.

This module provides WebDriver management functionality for UI testing.
It supports local and remote WebDriver initialization with various browsers.
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.utils import logger
log = logger.customLogger()


class WebDriverManager:
    """WebDriver Manager for handling browser initialization and configuration."""

    def __init__(self):
        """Initialize WebDriver Manager with environment configuration."""
        self.browser = os.getenv('BROWSER', 'chrome')
        self.headless = os.getenv('HEADLESS', 'False').lower() == 'true'
        self.implicit_wait = int(os.getenv('IMPLICIT_WAIT', '10'))
        self.driver = None
        log.info(f"Initialized WebDriver Manager with browser: {self.browser}, headless: {self.headless}")

    def initialize_driver(self, remote=False):
        """
        Initialize WebDriver instance.

        Args:
            remote (bool, optional): Whether to use remote WebDriver. Defaults to False.

        Returns:
            webdriver: WebDriver instance
        """
        if remote:
            return self._initialize_remote_driver()
        else:
            return self._initialize_local_driver()

    def _initialize_local_driver(self):
        """
        Initialize local WebDriver instance.

        Returns:
            webdriver: Local WebDriver instance
        """
        log.info(f"Initializing local {self.browser} WebDriver")
        
        if self.browser.lower() == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--log-level=3")  # Suppress warnings
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
        
        elif self.browser.lower() == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        
        elif self.browser.lower() == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            
            self.driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )
        
        else:
            log.error(f"Unsupported browser: {self.browser}")
            raise ValueError(f"Unsupported browser: {self.browser}")
        
        # Configure WebDriver
        self.driver.maximize_window()
        self.driver.implicitly_wait(self.implicit_wait)
        
        log.info(f"Initialized local {self.browser} WebDriver")
        return self.driver

    def _initialize_remote_driver(self):
        """
        Initialize remote WebDriver instance for cloud testing.

        Returns:
            webdriver: Remote WebDriver instance
        """
        log.info(f"Initializing remote {self.browser} WebDriver")

        remote_url = os.getenv('REMOTE_URL')
        if not remote_url:
            log.error("Remote URL not configured in environment")
            raise ValueError("Remote URL not configured in environment")

        options = self._get_browser_options()



        # Add BrowserStack specific capabilities
        if "browserstack" in remote_url.lower():
            bs_options = {
                "userName": os.getenv('BS_USERNAME'),
                "accessKey": os.getenv('BS_ACCESS_KEY'),
                "resolution": os.getenv('RESOLUTION', '1920x1080'),
                "projectName": "Automation Framework",
                "buildName": "Build 1.0",
                "sessionName": f"{self.browser} Test",
                "local": "false",
                "seleniumVersion": "4.0.0",
            }

            if self.browser.lower() in ["chrome", "firefox", "edge"]:
                options.set_capability("browserName", self.browser.lower())
                options.set_capability("browserVersion", os.getenv('BROWSER_VERSION', 'latest'))
                options.set_capability("platformName", os.getenv('PLATFORM', 'Windows'))
                options.set_capability("bstack:options", bs_options)



        # Add LambdaTest specific capabilities
        elif "lambdatest" in remote_url.lower():
            lt_options = {
                "username": os.getenv('BS_USERNAME'),  # Reusing the same env vars
                "accessKey": os.getenv('BS_ACCESS_KEY'),
                "resolution": os.getenv('RESOLUTION', '1920x1080'),
                "project": "Automation Framework",
                "build": "Build 1.0",
                "name": f"{self.browser} Test",
                "selenium_version": "4.0.0",
            }

            if self.browser.lower() in ["chrome", "firefox", "edge"]:
                options.set_capability("browserName", self.browser.lower())
                options.set_capability("browserVersion", os.getenv('BROWSER_VERSION', 'latest'))
                options.set_capability("platformName", os.getenv('PLATFORM', 'Windows'))
                options.set_capability("LT:Options", lt_options)

        # Initialize remote WebDriver
        self.driver = webdriver.Remote(
            command_executor=remote_url,
            options=options
        )

        # Configure WebDriver
        self.driver.implicitly_wait(self.implicit_wait)

        log.info(f"Initialized remote {self.browser} WebDriver")
        return self.driver

    # def _initialize_remote_driver(self):
    #     """
    #     Initialize remote WebDriver instance for cloud testing.
    #
    #     Returns:
    #         webdriver: Remote WebDriver instance
    #     """
    #     log.info(f"Initializing remote {self.browser} WebDriver")
    #
    #     remote_url = os.getenv('REMOTE_URL')
    #     if not remote_url:
    #         log.error("Remote URL not configured in environment")
    #         raise ValueError("Remote URL not configured in environment")
    #
    #     capabilities = {
    #         "browserName": self.browser.lower(),
    #         "browserVersion": os.getenv('BROWSER_VERSION', 'latest'),
    #         "platformName": os.getenv('PLATFORM', 'Windows'),
    #     }
    #
    #     # Add BrowserStack specific capabilities
    #     if "browserstack" in remote_url.lower():
    #         bs_options = {
    #             "userName": os.getenv('BS_USERNAME'),
    #             "accessKey": os.getenv('BS_ACCESS_KEY'),
    #             "resolution": os.getenv('RESOLUTION', '1920x1080'),
    #             "projectName": "Automation Framework",
    #             "buildName": "Build 1.0",
    #             "sessionName": f"{self.browser} Test",
    #             "local": "false",
    #             "seleniumVersion": "4.0.0",
    #         }
    #         capabilities["bstack:options"] = bs_options
    #
    #     # Add LambdaTest specific capabilities
    #     elif "lambdatest" in remote_url.lower():
    #         lt_options = {
    #             "username": os.getenv('BS_USERNAME'),  # Reusing the same env vars
    #             "accessKey": os.getenv('BS_ACCESS_KEY'),
    #             "resolution": os.getenv('RESOLUTION', '1920x1080'),
    #             "project": "Automation Framework",
    #             "build": "Build 1.0",
    #             "name": f"{self.browser} Test",
    #             "selenium_version": "4.0.0",
    #         }
    #         capabilities["LT:Options"] = lt_options
    #
    #     # Initialize remote WebDriver
    #     self.driver = webdriver.Remote(
    #         command_executor=remote_url,
    #         options=self._get_browser_options(),
    #         desired_capabilities=capabilities
    #     )
    #
    #     # Configure WebDriver
    #     self.driver.implicitly_wait(self.implicit_wait)
    #
    #     log.info(f"Initialized remote {self.browser} WebDriver")
    #     return self.driver

    def _get_browser_options(self):
        """
        Get browser-specific options.

        Returns:
            Options: Browser options
        """
        if self.browser.lower() == "chrome":
            options = ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            return options
        
        elif self.browser.lower() == "firefox":
            options = FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")
            return options
        
        elif self.browser.lower() == "edge":
            options = EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            return options
        
        else:
            return None

    def quit_driver(self):
        """Quit WebDriver instance."""
        if self.driver:
            log.info("Quitting WebDriver...........")
            self.driver.quit()
            self.driver = None
