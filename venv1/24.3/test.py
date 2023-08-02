import requests

url = 'https://petstore.swagger.io/v2'
res = requests.get(f'{url}/pet/findByStatus?status=available')


print(res.status_code)
print(res.json())
# print(res.status_code)
# print(res.text)
# print(type(res.text))
# print(res.json())
# print(type(res.json()))
