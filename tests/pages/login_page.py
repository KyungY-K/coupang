from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

class LoginPage:
    URL = "https://www.coupang.com"
    EMAIL_INPUT_ID = "login-email-input"
    PASSWORD_INPUT_ID = "login-password-input"
    LOGIN_BUTTON_CLASS = "_loginSubmitButton"

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def input_email_and_password(self, email: str, password: str):
        email_input = self.driver.find_element(By.ID, self.EMAIL_INPUT_ID)
        email_input.send_keys(email)

        password_input = self.driver.find_element(By.ID, self.PASSWORD_INPUT_ID)
        password_input.send_keys(password)

    def submit_login(self):
        login_button = self.driver.find_element(By.CLASS_NAME, self.LOGIN_BUTTON_CLASS)
        login_button.click()