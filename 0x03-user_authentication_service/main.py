import requests

# Constants
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

BASE_URL = "http://127.0.0.1:5000"


# Helper function to make requests and validate responses
def make_request(
        method, endpoint, data=None, headers=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(method, url, data=data, headers=headers)
    assert (response.status_code == expected_status), \
        f"Unexpected status code: {response.status_code}"
    return response.json()


# Task functions
def register_user(email, password):
    data = {"email": email, "password": password}
    make_request("POST", "/users", data=data)


def log_in_wrong_password(email, password):
    data = {"email": email, "password": password}
    make_request("POST", "/sessions", data=data, expected_status=401)


def log_in(email, password):
    data = {"email": email, "password": password}
    response = make_request("POST", "/sessions", data=data)
    return response["session_id"]


def profile_unlogged():
    make_request("GET", "/profile", expected_status=403)


def profile_logged(session_id):
    headers = {"Cookie": f"session_id={session_id}"}
    make_request("GET", "/profile", headers=headers)


def log_out(session_i):
    headers = {"Cookie": f"session_id={session_id}"}
    make_request("DELETE", "/sessions", headers=headers)


def reset_password_token(email):
    data = {"email": email}
    response = make_request("POST", "/reset_password", data=data)
    return response["reset_token"]


def update_password(
        email,
        reset_token,
        new_password
):
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password}
    make_request("PUT", "/reset_password", data=data)


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
