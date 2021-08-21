import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect")
length_history = len(response.history)
print(f"количество редиректов - {length_history}")
print(f"итоговый редирект - {response.url}")
