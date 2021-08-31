import requests


class Test11:

    def test_check_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.post(url)
        print(dict(response.cookies))

        cookie_value = response.cookies.get('HomeWork')
        print(f"print cookie_value {cookie_value}")

        expected_cookie_value = 'hw_value'
        actual_cookie_value = response.cookies.get('HomeWork')
        assert actual_cookie_value == expected_cookie_value, "Actual cookie_value is not correct"




