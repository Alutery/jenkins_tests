import requests
import string
import random


url = r'http://localhost:8080/securityRealm/createAccount'
headers = {'content-type': 'application/x-www-form-urlencoded'}


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))


def clear_user(user):
    from selenium import webdriver
    import time

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('http://localhost:8080/login')
    password = 'PASSWORD'

    driver.find_element_by_id('j_username').send_keys('admin')
    driver.find_element_by_name('j_password').send_keys(password)
    driver.find_element_by_name('Submit').click()

    url_tmp = 'http://localhost:8080/securityRealm/user/' + user + '/delete'
    driver.get(url_tmp)
    driver.find_element_by_id('yui-gen2-button').click()

    time.sleep(5)
    driver.close()
    driver.quit()


def create_data(username, fullname, email, password1):
    data = {
        "username": username,
        "fullname": fullname,
        "email": email,
        "password1": password1,
        "password2": password1,
        "Submit": "Create account"
    }
    print(data)
    print()
    return data


def test_response_code_200():
    response = requests.get('http://localhost:8080/signup')
    assert response.status_code == 200


def test_success():
    username = "user" + random_string()
    data = create_data(username, "User Test", "test@mail.ru", "1234")

    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html;charset=utf-8'
    assert "Success" in response.text

    clear_user(username)


def test_invalid_email():
    data = create_data("user" + random_string(), "User Test", "test", "1234")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert "Email - Invalid e-mail address" in response.text


def test_empty_email():
    data = create_data("user" + random_string(), "User Test", "", "1234")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert "Email - Invalid e-mail address" in response.text


def test_existed_username():
    data = create_data("User1", "User Test", "test@mail.ru", "1234")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert 'Username - User name is already taken' in response.text


def test_invalid_symbols_username():
    data = create_data("\\", "User Test", "test@mail.ru", "1234")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert 'Username - User name must only contain alphanumeric characters, underscore and dash' in response.text


def test_empty_username():
    data = create_data("", "User Test", "test@mail.ru", "1234")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert 'Username - "" is prohibited as a username for security reasons.' in response.text


def test_empty_password():
    data = create_data("user" + random_string(), "User Test", "test@mail.ru", "")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert "Password - Password is required" in response.text


def test_empty_fullname():
    data = create_data("user" + random_string(), "", "test@mail.ru", "")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert "Success" not in response.text
    assert "You are now logged in." not in response.text
