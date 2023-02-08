# Traff Monetizer API

UNOFFICIAL Python bindings for Traff Monetizer Dashboard API

## Installation

```BASH
pip install pyTraffMonetizer
```

## Usage

---

### Login with email and password:

```PYTHON
from pyTraffMonetizer import TraffMonetizer

# Your TraffMonetizer login email and password
EMAIL = ""
PASSWORD = ""
g_captcha_response = "" # I haven't figured out how to use this (so this function is actually unusable)

# Initialise the TraffMonetizer object
user = TraffMonetizer()

# Optionally, when instantiating you can pass in the following attributes to the TraffMonetizer class:
```

| Attribute      | Description        | Default Value                   |
|----------------|--------------------|---------------------------------|
| API_BASE_URL | The API BASE URL | https://data.traffmonetizer.com                            |
| API_PREFIX | The API PREFIX | /api                            |
| API_VERSION | The API VERSION | ""                            |

```PYTHON
# Call the complete_login_flow method to login and set the JWT in self.jwt
user.complete_login_flow(USERNAME, PASSWORD, g_captcha_response)
```

---

### Add proxies for future requests:

```PYTHON
from pyTraffMonetizer import TraffMonetizer

# With authentication & protocol
user.set_proxy("ip:port:username:password", "socks5")

# Without authentication & protocol
user.set_proxy("ip:port", "socks5")

# Alternative way
user.set_socks5_proxy("ip:port")
user.set_socks5_proxy("ip:port:username:password")
user.set_https_proxy("ip:port")
user.set_https_proxy("ip:port:username:password")
```

## Functions

---

1. Get user balance

    ```PYTHON
    # Get balance and traffic sold as shown on the dashboard.
    user.get_balance()
    ```
---

2. Remove a proxy

    ```PYTHON
    # Removes a proxy for future requests.
    user.remove_proxy()
    ```
---

3. Get all the devices

    ```PYTHON
    # Get all the devices (with earnings)
    user.get_earnings_by_devices()
    ```
---

4. Payout history

    ```PYTHON
    # Get payout history
    user.get_payout_history()
    ```
---

5. Is Logged In

    ```PYTHON
    # Check if you're logged in
    user.is_logged_in()
    ```
---

6. Logout

    ```PYTHON
    # Logged out
    user.logout()
    ```
---

7. Set JWT Token

    ```PYTHON
    # Set JWT Token if you have one (otherwise use the login())
    user.set_jwt_token(TOKEN)
    ```
---

## Exceptions

- The following exceptions are defined.
    Exception | Reason
    --- | ---
    `NotLoggedInError` | Raised when you try to access protected routes (dashboard, payout history, etc).
---

## Liked my work?

---

Consider donating:

- BTC: bc1qu98aj9etma5l64lcfldweua7w8gnjzets05v6p

- LTC: LiTzM41bD1ewPAjFxcGyNDZXFYXqUS9fXK

