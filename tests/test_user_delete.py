import time

import allure
from allure_commons.types import Severity

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Delete cases")
@allure.tag("Delete")
class TestUserDelete(BaseCase):

    @allure.description("This test check do not delete test users with ID  2")
    @allure.severity(Severity.NORMAL)
    def test_delete_user_with_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # LOGIN
        with allure.step('Login user with id 2'):
            response1 = MyRequests.post("/user/login", data=data)
        print(f"ответ запроса /user/login - {response1.content}")

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        print(user_id_from_auth_method)

        # DELETE
        with allure.step('Delete user with id 2'):
            response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid}
                                          )
        print(f"ответ запроса /user/{user_id_from_auth_method} - {response2.content}")
        print(response2.status_code)

        Assertions.assert_code_status(response2, 400)
        Assertions.assert_response_content(response2, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

        # GET
        with allure.step('Get user with id 2'):
            response3 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response3, expected_fields)

    @allure.description("This test check delete just created user")
    @allure.severity(Severity.CRITICAL)
    def test_delete_just_created_user(self):
        # REGISTER

        register_data = self.prepare_registration_data()
        with allure.step('Register new user'):
            response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id_from_auth_method = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step('Login user just created'):
            response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        with allure.step('Delete user just created'):
            response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid}
                                          )
        print(f"ответ запроса /user/{user_id_from_auth_method} - {response2.content}")
        print(response2.status_code)

        Assertions.assert_code_status(response2, 200)

        # GET
        with allure.step('Get user just created and deleted'):
            response3 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_response_content(response3, 'User not found')

    @allure.description("This test check not delete user with authorization other user")
    @allure.severity(Severity.CRITICAL)
    def test_delete_user_with_authorization_other_user(self):
        # REGISTER USER1
        register_data = self.prepare_registration_data()
        with allure.step('Register new user1'):
            response1_1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1_1, 200)
        Assertions.assert_json_has_key(response1_1, "id")

        email1 = register_data['email']
        first_name1 = register_data['firstName']
        password1 = register_data['password']
        user_id1 = self.get_json_value(response1_1, "id")
        print(f"id первого пользователя {user_id1}")

        time.sleep(1)

        # REGISTER USER2
        register_data = self.prepare_registration_data()
        with allure.step('Register new user2'):
            response1_2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1_2, 200)
        Assertions.assert_json_has_key(response1_2, "id")

        email2 = register_data['email']
        first_name2 = register_data['firstName']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response1_2, "id")
        print(f"id второго пользователя {user_id2}")

        # LOGIN USER1
        login_data = {
            'email': email1,
            'password': password1
        }

        with allure.step('Login user1 just created'):
            response2_1 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response2_1, "auth_sid")
        token1 = self.get_header(response2_1, "x-csrf-token")
        print(f"ответ по первому пользователю /user/login {response2_1.content}")

        # LOGIN USER2
        login_data = {
            'email': email2,
            'password': password2
        }
        with allure.step('Login user2 just created'):
            response2_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid2 = self.get_cookie(response2_2, "auth_sid")
        token2 = self.get_header(response2_2, "x-csrf-token")
        print(f"ответ по второму пользователю /user/login {response2_2.content}")

        # DELETE USER2 WITH TOKEN,COOKIE USER1
        new_name = "Changed Name"
        with allure.step('Delete user2 with token and cookie user1'):
            response3 = MyRequests.delete(
                f"/user/{user_id2}",
                headers={"x-csrf-token": token1},
                cookies={"auth_sid": auth_sid1},
                data={"firstName": new_name}
            )

        Assertions.assert_code_status(response3, 200)
        print(f"удаление второго пользователя с токеном первого ответ {response3.content}")

        # GET INFO USER2_ CHECK NAME CORRECT WITHOUT CHANGE IN EDIT METHOD
        with allure.step('Get info user2 and check name correct without edit'):
            response4 = MyRequests.get(
                f"/user/{user_id2}",
                headers={"x-csrf-token": token2},
                cookies={"auth_sid": auth_sid2},
            )
        print(f"ответ по четвертому запросу {response4.content}")
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name2,
            "Wrong name of the user after edit"
        )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email2,
            "Wrong email of the user after edit"
        )
