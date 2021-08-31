import requests


class Test11:

    def test_check_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_header"

        response = requests.post(url)
        print(f"ответ запроса response {response.headers}")

        header_value_x_secret_homework_header = response.headers.get('x-secret-homework-header')

        print(f"print header ¨x_secret_homework_header¨ {header_value_x_secret_homework_header}")

        expected_header_x_secret_homework_header = 'x-secret-homework-header'
        expected_header_value_x_secret_homework_header = 'Some secret value'
        actual_header_value_x_secret_homework_header = response.headers.get('x-secret-homework-header')

        assert expected_header_x_secret_homework_header in response.headers, "There is no header 'x-secret-homework-header' in response"
        assert actual_header_value_x_secret_homework_header == expected_header_value_x_secret_homework_header, "Actual header_value 'x-secret-homework-header' is not correct"




