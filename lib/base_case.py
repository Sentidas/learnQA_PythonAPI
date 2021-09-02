import json
import random
import string
from datetime import datetime

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecoderError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_registration_data_with_name(self, firstname=None, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        if firstname is None:
            firstname = 'learnqa'
        return {
            'password': '1234',
            'username': 'learnqa',
            'firstName': firstname,
            'lastName': 'learnqa',
            'email': email
        }

    def generate_random_string(self, length):
        letters = string.ascii_uppercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        # print("Random string of length", length, "is:", rand_string)
        return rand_string

    def prepare_registration_data_witout_params(self, params, email=None):

        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        params_dict = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        print(f"передаваемый параметр - {params}")
        print(f"Возвращаемый словарь - {params_dict}")
        del params_dict[params]
        print(f"Возвращаемый словарь с удалением  - {params_dict} при удалении параметра  {params}")

        return params_dict


