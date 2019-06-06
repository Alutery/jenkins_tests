from my_jenkins.locators.locators import Locators


class SignupPage:

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        self.driver.find_element_by_id(Locators.username_input_id).clear()
        self.driver.find_element_by_id(Locators.username_input_id).send_keys(username)

    def enter_fullname(self, fullname):
        self.driver.find_element_by_id(Locators.fullname_input_id).clear()
        self.driver.find_element_by_id(Locators.fullname_input_id).send_keys(fullname)

    def enter_email(self, email):
        self.driver.find_element_by_id(Locators.email_input_id).clear()
        self.driver.find_element_by_id(Locators.email_input_id).send_keys(email)

    def enter_password1(self, password1):
        self.driver.find_element_by_id(Locators.password1_input_id).clear()
        self.driver.find_element_by_id(Locators.password1_input_id).send_keys(password1)

    def click_submit(self):
        self.driver.find_element_by_name(Locators.submit_input_name).click()

    def click_show_password(self):
        self.driver.find_element_by_class_name(Locators.checkbox_class_name).click()
