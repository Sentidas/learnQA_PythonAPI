import time

import allure
from allure_commons.types import Severity

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Edit cases")
@allure.tag("Edit")
class TestUserEdit(BaseCase):

    @allure.description("This test check edit name of just created user")
    @allure.severity(Severity.BLOCKER)
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step('Register new user'):
            response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step('Login just created user'):
            response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        with allure.step('Change name of just created user'):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )
        print(f"ответ /user/{user_id} - {response3.content}")
        Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step('Get info (name) of just created and edit user'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test check no edit just created user without_authorization")
    @allure.severity(Severity.CRITICAL)
    def test_edit_just_created_user_without_authorization(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step('Register new user'):
            response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed Name"
        with allure.step('Change name of just created user without token and cookie'):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                data={"firstName": new_name}
            )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_content(response3, 'Auth token not supplied')

        # LOGIN FOR CHECK DATA USER WITH METHOD GET
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step('Login for check data user'):
            response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # GET
        with allure.step('Get for check name user without edit'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test check no edit with incorrect email")
    @allure.severity(Severity.NORMAL)
    def test_edit_just_created_user_with_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step('Register new user'):
            response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step('Login just created user'):
            response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "Changed.yandex.ru"
        with allure.step('Change email to incorrect email'):
            response3 = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_email}
            )
        print(f"ответ /user/{user_id} - {response3.content}")
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_content(response3, 'Invalid email format')

        # GET
        with allure.step('Get for check name user without edit'):
            response4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        Assertions.assert_json_value_by_name(
            response4,
            "email",
            email,
            "Incorrect mail was changed"
        )

    @allure.description("This test check edit just created user without_authorization")
    @allure.severity(Severity.NORMAL)
    def test_edit_just_created_user_with_short_name(self):

        # REGISTER
        register_data = self.prepare_registration_data()
        with allure.step('Register new user'):
          response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step('Login new user'):
          response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT USER
        new_name = self.generate_random_string(1)
        with allure.step('Edit new user'):
          response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        print(f"ответ /user/{user_id} - {response3.content}")
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_text_in_value(self.get_json_value(response3, "error"), "Too short value for field firstName")

        # GET
        with allure.step('Get new user'):
           response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            first_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test check edit just created user with authorization other user")
    @allure.severity(Severity.CRITICAL)
    def test_edit_just_created_user_with_authorization_other_user(self):

        # REGISTER USER1
        with allure.step('Register new user1'):
          register_data = self.prepare_registration_data()

        response1_1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1_1, 200)
        Assertions.assert_json_has_key(response1_1, "id")

        email1 = register_data['email']
        first_name1 = register_data['firstName']
        password1 = register_data['password']
        user_id1 = self.get_json_value(response1_1, "id")
        print(f"id первого пользователя {user_id1}")

        time.sleep(2)

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
        with allure.step('Login new user1'):
          response2_1 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response2_1, "auth_sid")
        token1 = self.get_header(response2_1, "x-csrf-token")
        print(f"ответ по первому пользователю /user/login {response2_1.content}")

        # LOGIN USER2
        login_data = {
            'email': email2,
            'password': password2
        }
        with allure.step('Login new user2'):
          response2_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid2 = self.get_cookie(response2_2, "auth_sid")
        token2 = self.get_header(response2_2, "x-csrf-token")
        print(f"ответ по второму пользователю /user/login {response2_2.content}")

        # EDIT USER2 WITH USER1'S TOKEN,COOKIE"
        new_name = "Changed Name"
        with allure.step('Edit user2 with token and cookie of user1'):
          response3 = MyRequests.put(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET INFO USER2_CHECK NAME CORRECT WITHOUT CHANGE IN EDIT METHOD
        with allure.step('Get info user2 to check name correct with change'):
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
