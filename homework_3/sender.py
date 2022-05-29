import requests


while True:
    userName = input("Введите имя: ")
    while True:
        userMessage = input("Введите сообщение: ")

        userMessageAsJson = {
            "userName": f"{userName}",
            "userMessage": f"{userMessage}"
        }
        requests.post('http://localhost:8080/sendMessage', json=userMessageAsJson)
        break
