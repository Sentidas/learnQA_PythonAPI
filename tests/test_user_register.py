import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Authorization cases")
class TestUserRegister(BaseCase):
    exclude_params = {
        "password",
        "username",
        "firstName",
        "lastName",
        "email"
    }

    @allure.description("This test unsuccessfully registration with incorrect email - without '@'")
    def test_create_user_with_incorrect_email(self):
        data = self.prepare_registration_data('vinkotovexample.com')

        response = MyRequests.post("/user/", data=data)
        print(response.content)
        print(response.status_code)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    @allure.description("This test unsuccessfully registration with incorrect firstName with 1 symbol")
    def test_create_user_with_name1(self):
        name_random = self.generate_random_string(1)
        print(f"print name {name_random}")
        data = self.prepare_registration_data_with_name(name_random)

        response = MyRequests.post("/user/", data=data)
        print(response.content)
        print(response.status_code)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "The value of 'firstName' field is too short")

    @allure.description("This test unsuccessfully registration with incorrect firstName with > 250 symbols")
    def test_create_user_with_name251(self):
        name_random = self.generate_random_string(251)
        print(f"print name {name_random}")
        data = self.prepare_registration_data_with_name(name_random)

        response = MyRequests.post("/user/", data=data)
        print(response.content)
        print(response.status_code)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, "The value of 'firstName' field is too long")

    @allure.description(f"This test unsuccessfully registration without one of params - {exclude_params}")
    @pytest.mark.parametrize('exclude_params', exclude_params)
    def test_create_user_with_one_of_params(self, exclude_params):
        data = self.prepare_registration_data_witout_params(exclude_params)

        response = MyRequests.post("/user/", data=data)
        print(response.content)
        print(response.status_code)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"The following required params are missed: {exclude_params}")

    @allure.description("This test successfully registration for new user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        print(response.content)
        print(response.status_code)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test unsuccessfully registration with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        print(response.status_code)
        print(response.content)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")