import json

string_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

obj = json.loads(string_text)
print(obj['messages'])

second_message = obj['messages'][1]
print(second_message)






