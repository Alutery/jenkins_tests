import requests


url = 'http://localhost:8080/j_acegi_security_check'
headers = {'content-type': 'application/x-www-form-urlencoded'}


def create_data(j_username, j_password, from_input='/'):
    data = {
        'j_username': j_username,
        'j_password': j_password,
        'from': from_input,
        'Submit': 'Sign in'
    }

    return data


def test_login_success():
    data = create_data("User1", "1234")

    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html;charset=utf-8'
    assert 'log out' in response.text


def test_invalid_username():
    data = create_data("userrrrr", "1234")

    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'text/html;charset=utf-8'
    assert 'Invalid username or password' in response.text


def test_invalid_password():
    data = create_data("User1", "123456")

    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'text/html;charset=utf-8'
    assert 'Invalid username or password' in response.text


def test_invalid_from():
    data = create_data('User1', '1234', '/++++')

    response = requests.post(url, params=data, headers=headers)

    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'text/html;charset=iso-8859-1'
    assert 'Not Found' in response.text
