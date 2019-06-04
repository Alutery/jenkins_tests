import pytest
import time
from selenium import webdriver
from my_jenkins.pages.signup import SignupPage
import random
import string


def random_string(string_length=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))


@pytest.fixture(scope='module')
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver

    time.sleep(4)
    driver.close()
    driver.quit()


@pytest.fixture(scope='module')
def signup_page(driver):
    signup = SignupPage(driver)

    return signup


def input_data(signup_page, username, fullname, email, password1):
    signup_page.enter_username(username)
    signup_page.enter_fullname(fullname)
    signup_page.enter_email(email)
    signup_page.enter_password1(password1)


def test_signup_page(driver):
    driver.get("http://localhost:8080/signup")
    assert "Create an account! [Jenkins]" == driver.title
    assert "Not Found" not in driver.page_source


def test_valid_signup(driver, signup_page):
    driver.get("http://localhost:8080/signup")
    input_data(signup_page, "user" + random_string(), "User New", "new@gmail.com", "1234")
    signup_page.click_submit()
    assert "Jenkins" == driver.title
    assert "Success" in driver.page_source
    assert "You are now logged in." in driver.page_source


def test_existed_username(driver, signup_page):
    driver.get("http://localhost:8080/signup")
    input_data(signup_page, "User1", "User New", "new@gmail.com", "1234")
    signup_page.click_submit()
    assert driver.find_element_by_xpath('//label[@for="username"]').text == "Username - User name is already taken"


def test_invalid_symbols_username(driver, signup_page):
    driver.get("http://localhost:8080/signup")
    input_data(signup_page, "User^_^", "User New", "new@gmail.com", "1234")
    signup_page.click_submit()
    assert driver.find_element_by_xpath('//label[@for="username"]').text == "Username - User name must only contain alphanumeric characters, underscore and dash"


def test_empty_username(driver, signup_page):
    driver.get("http://localhost:8080/signup")
    input_data(signup_page, "", "User New", "new@gmail.com", "1234")
    signup_page.click_submit()
    assert driver.find_element_by_xpath('//label[@for="username"]').text == 'Username - "" is prohibited as a username for security reasons.'


def test_invalid_email(driver, signup_page):
    driver.get("http://localhost:8080/signup")
    input_data(signup_page, "User", "User New", "new", "1234")
    signup_page.click_submit()
    assert driver.find_element_by_xpath('//label[@for="email"]').text == "Email - Invalid e-mail address"


def test_empty_password1(driver, signup_page):
    driver.get("http://localhost:8080/signup")
    input_data(signup_page, "User", "User New", "new", "")
    signup_page.click_submit()
    assert driver.find_element_by_xpath('//label[@for="password1"]').text == "Password - Password is required"