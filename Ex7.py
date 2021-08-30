import requests


response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"1. Eсли делаем http-запрос любого типа без параметра method, выводится - '{response.text}'. Cо статус-кодом ответа - {response.status_code}")
method = {"method":"HEAD"}
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method)
print(f"2. Eсли делаем http-запрос не из списка, например, HEAD, выводится - '{response.text}'. Cо статус-кодом ответа - {response.status_code}")
method = {"method":"GET"}
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method)
print(f"3.1 Eсли делаем запрос {method['method']} с правильным значением method, выводится - '{response.text}'. Cо статус-кодом ответа - {response.status_code}")
method = {"method":"POST"}
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method)
print(f"3.2 Eсли делаем запрос {method['method']} с правильным значением method, выводится - '{response.text}'. Cо статус-кодом ответа - {response.status_code}")
method = {"method":"PUT"}
response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method)
print(f"3.3 Eсли делаем запрос {method['method']} с правильным значением method, выводится - '{response.text}'. Cо статус-кодом ответа - {response.status_code}")
method = {"method":"DELETE"}
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method)
print(f"3.4 Eсли делаем запрос {method['method']} с правильным значением method, выводится - '{response.text}'. Cо статус-кодом ответа - {response.status_code}")




url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
map = [
    {'method': 'GET'},
    {'method': 'POST'},
    {'method': 'PUT'},
    {'method': 'DELETE'},
]

i = 0
for each in map:
    requests.get(url, params=each)
    print(f"ответы для запросов get и метода {map[i]['method']} {requests.post(url, params=each).text}")
    i= i+1


i = 0
for each in map:
    requests.post(url, data=each)
    print(f"ответы для запросов post и метода {map[i]['method']} {requests.post(url, data=each).text}")
    i= i+1

i = 0
for each in map:
    requests.put(url, data=each)
    print(f"ответы для запросов put и метода {map[i]['method']} {requests.put(url, data=each).text}")
    i= i+1


i = 0
for each in map:
    requests.delete(url, data=each)
    print(f"ответы для запросов delete и метода {map[i]['method']} {requests.delete(url, data=each).text}")
    i= i+1


