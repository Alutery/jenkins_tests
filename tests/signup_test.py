import pytest
import time
from selenium import webdriver
from my_jenkins.pages.signup import SignupPage
import random
import string


url = 'http://localhost:8080/signup'
users_signup = []


def random_string(string_length=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))


def clear_users():
    driver.get('http://localhost:8080/login')
    password = 'PASSWORD'

    driver.find_element_by_id('j_username').send_keys('admin')
    driver.find_element_by_name('j_password').send_keys(password)
    driver.find_element_by_name('Submit').click()

    for user in users_signup:
        url_tmp = 'http://localhost:8080/securityRealm/user/' + user + '/delete'
        driver.get(url_tmp)
        driver.find_element_by_id('yui-gen2-button').click()


@pytest.fixture(scope='module')
def driver():
    users_signup.clear()
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    # driver.maximize_window()

    yield driver

    # clear_users()
    time.sleep(20)
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
    driver.get(url)
    assert "Create an account! [Jenkins]" == driver.title
    assert "Not Found" not in driver.page_source

    assert not driver.find_element_by_id('passwordStrengthWrapper').is_displayed()
    assert driver.find_element_by_xpath('//label[@for="username"]').text == 'Username'
    assert driver.find_element_by_xpath('//label[@for="fullname"]').text == 'Full name'
    assert driver.find_element_by_xpath('//label[@for="email"]').text == 'Email'
    assert driver.find_element_by_xpath('//label[@for="password1"]').text == 'Password'
    assert driver.find_element_by_xpath('//input[@name="Submit"]').get_attribute('value') == 'Create account'


def test_valid_signup(driver, signup_page):
    driver.get(url)
    username = "User" + random_string()
    input_data(signup_page, username, "User New", "user@mail.com", "1234")
    signup_page.click_submit()

    assert "Jenkins" == driver.title
    assert "Success" in driver.page_source
    assert "You are now logged in." in driver.page_source

    users_signup.append(username)


def test_existed_username(driver, signup_page):
    driver.get(url)
    input_data(signup_page, "User1", "User New", "user@mail.com", "1234")
    signup_page.click_submit()

    assert driver.find_element_by_xpath('//label[@for="username"]').text == "Username - User name is already taken"


def test_invalid_symbols_username(driver, signup_page):
    driver.get(url)
    input_data(signup_page, "User^_^", "User New", "user@mail.com", "1234")
    signup_page.click_submit()

    assert driver.find_element_by_xpath('//label[@for="username"]').text == "Username - User name must only contain alphanumeric characters, underscore and dash"


def test_empty_username(driver, signup_page):
    driver.get(url)
    input_data(signup_page, "", "User New", "user@mail.com", "1234")
    signup_page.click_submit()

    assert driver.find_element_by_xpath('//label[@for="username"]').text == 'Username - "" is prohibited as a username for security reasons.'


def test_invalid_email(driver, signup_page):
    driver.get(url)
    input_data(signup_page, "User" + random_string(), "User New", "new", "1234")
    signup_page.click_submit()

    assert driver.find_element_by_xpath('//label[@for="email"]').text == "Email - Invalid e-mail address"


def test_empty_email(driver, signup_page):
    driver.get(url)
    input_data(signup_page, "User" + random_string(), "User New", "", "1234")
    signup_page.click_submit()

    assert driver.find_element_by_xpath('//label[@for="email"]').text == "Email - Invalid e-mail address"


def test_empty_password1(driver, signup_page):
    driver.get(url)
    input_data(signup_page, "User" + random_string(), "User New", "user@mail.com", "")
    signup_page.click_submit()

    assert driver.find_element_by_xpath('//label[@for="password1"]').text == "Password - Password is required"


def test_empty_fullname(driver, signup_page):
    driver.get(url)
    username = "User" + random_string()
    input_data(signup_page, username, "", "user@mail.com", "1234")
    signup_page.click_submit()

    assert "Jenkins" == driver.title
    assert "Success" in driver.page_source
    assert "You are now logged in." in driver.page_source

    users_signup.append(username)


def test_poor_password(driver, signup_page):
    driver.get(url)
    signup_page.enter_password1("1")

    assert driver.find_element_by_id('passwordStrengthWrapper').text == 'Strength: Poor'
    assert driver.find_element_by_id('passwordStrength').get_attribute('style') == 'color: rgb(196, 0, 10);'


def test_weak_password(driver, signup_page):
    driver.get(url)
    signup_page.enter_password1("123aaa")

    assert driver.find_element_by_id('passwordStrengthWrapper').text == 'Strength: Weak'
    assert driver.find_element_by_id('passwordStrength').get_attribute('style') == 'color: rgb(222, 89, 18);'


def test_moderate_password(driver, signup_page):
    driver.get(url)
    signup_page.enter_password1("1234asdASD")

    assert driver.find_element_by_id('passwordStrengthWrapper').text == 'Strength: Moderate'
    assert driver.find_element_by_id('passwordStrength').get_attribute('style') == 'color: rgb(198, 129, 14);'


def test_strong_password(driver, signup_page):
    driver.get(url)
    signup_page.enter_password1("1234asdASD#")

    assert driver.find_element_by_id('passwordStrengthWrapper').text == 'Strength: Strong'
    assert driver.find_element_by_id('passwordStrength').get_attribute('style') == 'color: rgb(58, 121, 17);'


def test_show_password(driver, signup_page):
    driver.get(url)

    signup_page.click_show_password()
    assert driver.find_element_by_id('password1').get_attribute('type') == 'text'

    signup_page.click_show_password()
    assert driver.find_element_by_id('password1').get_attribute('type') == 'password'
