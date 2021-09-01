import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
print(response.text)
seconds = response.json()["seconds"]
token = response.json()["token"]
print(f"seconds {seconds}")
print(f"token {token}")
response = requests.get(url, params={"token":token})
print(f"второй вывод, еще не отработал таймер {response.text}")
time.sleep(seconds)
response = requests.get(url, params={"token":token})
print(f"третий вывод, как отработал таймер {response.text}")