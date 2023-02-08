import requests

from .exceptions import *

class TraffMonetizer:
	def __init__(self, API_BASE_URL = "https://data.traffmonetizer.com", API_PREFIX = "/api", API_VERSION = "") -> None:
		"""Initialises TraffMonetizer class. """
		self.API_URL = API_BASE_URL + API_PREFIX + API_VERSION

		self.remove_all_headers()
		self.add_default_headers({
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
			"Origin": "https://app.traffmonetizer.com",
			"Referrer": "https://app.traffmonetizer.com",
		})

		self.remove_proxy()
		self.logout()

	def remove_all_headers(self) -> bool:
		"""Removes all default headers for future requests. """
		self.__headers = {}

	def add_default_headers(self, headers: dict = {}) -> bool:
		"""Adds default headers for future requests. Could be used to set user-agent for example. """
		self.__headers = {
			**self.__headers, **headers
		}

		return True

	def __return_response(self, response) -> dict:
		"""Return an easy to navigate dict. """
		result = {}

		result["json"] = None

		result["success"] = bool(response.ok)

		try:
			# Try this line, because you might not get a response everytime
			result["json"] = response.json()
		except:
			pass

		result["response"] = response

		return result

	def logout(self) -> bool:
		"""Sets JWT token to None. """
		return self.set_jwt_token(None)

	def __make_request(self, req_type: str, endpoint: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make requests. """

		return requests.request(req_type, f'{self.API_URL}{endpoint}', proxies = self.proxy_conf, headers = {
            **self.__headers, **headers, **({
                "Authorization": f"Bearer {self.jwt}",
            } if self.is_logged_in() else {}),
        }, *args, **kwargs)

	def set_proxy(self, proxy_str: str = None, protocol: str = "socks5") -> bool:
		"""Sets the proxy for future API requests."""

		if proxy_str is None:
			self.proxy_conf = None
			return True

		proxy = proxy_str.split(":")

		if len(proxy) > 2:
			ip, port, username, password = proxy

			self.proxy_conf = {
				"http": f"{protocol}://{username}:{password}@{ip}:{port}",
				"https": f"{protocol}://{username}:{password}@{ip}:{port}",
			}
		else:
			ip, port = proxy

			self.proxy_conf = {
				"http": f"{protocol}://{ip}:{port}",
				"https": f"{protocol}://{ip}:{port}",
			}

		return True

	def set_socks5_proxy(self, proxy_str: str = None) -> bool:
		"""Sets SOCKS5 proxy for future API requests. """
		return self.set_proxy(proxy_str, "socks5")

	def set_http_proxy(self, proxy_str: str = None) -> bool:
		"""Sets HTTP proxy for future API requests. """
		return self.set_proxy(proxy_str, "http")

	def set_https_proxy(self, proxy_str: str = None) -> bool:
		"""Sets HTTPS proxy for future API requests. """
		return self.set_proxy(proxy_str, "https")

	def remove_proxy(self) -> bool:
		"""Removes the proxy for future API requests. """
		return self.set_proxy(None)

	def __handle_not_logged_in(self) -> None:
		if not self.is_logged_in():
			raise NotLoggedInError

	def is_logged_in(self) -> bool:
		"""Returns if we're logged in or not. """
		return self.jwt is not None

	def set_jwt_token(self, jwt: str = None) -> bool:
		"""Sets the JWT token for future requests. """
		self.jwt = jwt
		return True

	def login(self, email: str, password: str, g_captcha_response: str = "") -> dict:
		"""Logs in into the TraffMonetizer dashboard. """

		response = self.__make_request("POST", "/auth/login", json = {
			"email": email,
			"g-recaptcha-response": g_captcha_response,
			"password": password,
		})

		return self.__return_response(response)

	def complete_login_flow(self, email: str, password: str, g_captcha_response: str) -> bool:
		login_result = self.login(email, password, g_captcha_response)

		if login_result["success"]:
			token = login_result["json"]["data"]["token"]

			self.set_jwt_token(token)

			return True

		return False

	def get_payout_settings(self) -> dict:
		"""Returns information about the payout settings for the logged in user. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/user/payout_settings/get")

		return self.__return_response(response)

	def get_graph_stat(self, period: str = "month") -> dict:
		"""Returns graph stat. """

		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/stat/get_earning_by_devices", params = {
			"period": period,
		})

		return self.__return_response(response)

	def get_earnings_by_devices(self, start_date: str, end_date: str, limit_count: int = 25, limit_start: int = 0) -> dict:
		"""Returns earnings by devices information. 
		start_date and end_date has format of: Tue Jan 31 2023
		"""
		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/stat/get_earning_by_devices", json = {
			"startDate": start_date,
			"limitCount": limit_count,
			"limitStart": limit_start,
			"endDate": end_date,
		})

		return self.__return_response(response)

	def get_balance(self) -> dict:
		"""Returns balance information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/app_user/get_balance")

		return self.__return_response(response)

	def get_payout_history(self, page: int = 1) -> dict:
		"""Returns payouts information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/payments/get_by_user")

		return self.__return_response(response)
	
	def get_invited_users(self) -> dict:
		"""Returns referrals information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/affiliate/get_invited_users")

		return self.__return_response(response)

	def get_referrer_earnings(self) -> dict:
		"""Returns referral earnings information. """
		self.__handle_not_logged_in()

		response = self.__make_request("GET", "/affiliate/get_referrer_earnings")

		return self.__return_response(response)

	def __repr__(self):
		"""Represents the TraffMonetizer object. """
		return f"<TraffMonetizer object at {hex(id(self))}>"
