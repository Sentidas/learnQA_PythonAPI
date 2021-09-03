import time

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
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

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        print(f"ответ /user/{user_id} - {response3.content}")
        Assertions.assert_code_status(response3, 200)

        # GET
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

    def test_edit_just_created_user_without_authorization(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed Name"
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

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # GET
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

    def test_edit_just_created_user_with_incorrect_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
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

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT

        new_email = "Changed.yandex.ru"
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

    def test_edit_just_created_user_with_short_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
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

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT USER2
        new_name = self.generate_random_string(1)
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

    def test_edit_just_created_user_with_authorization_other_user(self):
        # REGISTER USER1
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

        response2_1 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response2_1, "auth_sid")
        token1 = self.get_header(response2_1, "x-csrf-token")
        print(f"ответ по первому пользователю /user/login {response2_1.content}")

        # LOGIN USER2
        login_data = {
            'email': email2,
            'password': password2
        }

        response2_2 = MyRequests.post("/user/login", data=login_data)
        auth_sid2 = self.get_cookie(response2_2, "auth_sid")
        token2 = self.get_header(response2_2, "x-csrf-token")
        print(f"ответ по второму пользователю /user/login {response2_2.content}")

        # EDIT USER2 WITH TOKEN,COOKIE USER1
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET INFO USER2_ CHECK NAME CORRECT WITHOUT CHANGE IN EDIT METHOD
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
