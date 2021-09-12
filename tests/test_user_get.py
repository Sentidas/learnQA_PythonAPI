import time

import allure
from allure_commons.types import Severity

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Get cases")
@allure.tag("Get")
class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        print(response.content)
        print(response.status_code)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This test get user details with authorization as same user")
    @allure.severity(Severity.BLOCKER)
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step('Login user'):
          response1 = MyRequests.post("/user/login", data=data)
        print(f"ответ запроса /user/login - {response1.content}")
        print(response1.status_code)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step('Get details user'):
          response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        print(f"ответ запроса /user/{user_id_from_auth_method} - {response2.content}")
        print(response2.status_code)

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test get user details with authorization as other user")
    @allure.severity(Severity.BLOCKER)
    def test_get_user_details_auth_as_other_user(self):

        # REGISTER USER1
        register_data = self.prepare_registration_data()
        with allure.step('Register user1'):
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
        with allure.step('Register user2'):
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
        with allure.step('Logit user1'):
          response2_1 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response2_1, "auth_sid")
        token1 = self.get_header(response2_1, "x-csrf-token")
        print(f"ответ по первому пользователю /user/login {response2_1.content}")

        # LOGIN USER2
        login_data = {
            'email': email2,
            'password': password2
        }
        with allure.step('Logit user2'):
          response2_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid2 = self.get_cookie(response2_2, "auth_sid")
        token2 = self.get_header(response2_2, "x-csrf-token")
        print(f"ответ по второму пользователю /user/login {response2_2.content}")

        # GET INFO USER2 WITH TOKEN,COOKIE USER1
        with allure.step('Get details user2 with token and cookie of user1'):
           response4 = MyRequests.get(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
        )
        print(f"ответ по четвертому запросу {response4.content}")
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_has_key(response4, "username")
        Assertions.assert_json_has_not_key(response4, "email")
        Assertions.assert_json_has_not_key(response4, "firstName")
        Assertions.assert_json_has_not_key(response4, "lastName")
