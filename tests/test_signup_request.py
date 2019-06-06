import requests
import pytest
import string
import random


url = r'http://localhost:8080/securityRealm/createAccount'
headers = {'content-type': 'application/x-www-form-urlencoded'}


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(string_length))


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


def test_success():
    data = create_data("user" + random_string(), "ansafinaa", "qwerty@qwerty.ru", "q")

    response = requests.post(url, params=data, headers=headers)
    print(response.text)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html;charset=utf-8'


def test_response_code_200():
    response = requests.get(url)
    assert response.status_code == 200


def test_if_is_form_in_contact_page():
    pass
    # response = get_ulr_links('https://www.mulhergorila.com/contato/')
    # form = response.html.find('#gform_1', first=True)
    # assert 'Nome*\nE-mail*\nTelefone\nMensagem*' == form.text


# def test_password_not_match():
#     data = create_data("ansafinaa", "ansafinaa", "qwerty@qwerty.ru", "q", "qq")
#
#     response = requests.post(url, json=data, headers=headers)
#
#     print(response.headers)
#     print()
#     print(response.text)
#
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'text/html;charset=utf-8'


def test_invalid_email():
    data = create_data("ansafinaa", "ansafinaa", "qwertyqwertyru", "q")
    response = requests.post(url, params=data, headers=headers)

    assert "Email - Invalid e-mail address" in response.text


def test_invalid_username():
    data = create_data("\\", "ansafinaa", "qwertyqwertyru", "q")
    response = requests.post(url, params=data, headers=headers)

    assert 'Username - User name must only contain alphanumeric characters, underscore and dash' in response.text


def test_empty_username():
    data = create_data("", "ansafinaa", "qwertyqwertyru", "q")
    response = requests.post(url, params=data, headers=headers)

    assert 'Username - "" is prohibited as a username for security reasons.' in response.text


def test_empty_fullname():
    data = create_data("user" + random_string(), "", "qwerty@qwerty.ru", "q")
    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert 'Success' in response.text
    assert 'You are now logged in. Go back to <a href="..">the top page</a>' in response.text


