from datetime import datetime
from time import sleep

import requests

userDataAsJson = {
    "afterDate": "2018-05-29 00:30:39.697739"
}

while True:
    response = requests.get('http://localhost:8080/messages', json=userDataAsJson)
    messages = response.json()['messages']
    for message in messages:
        messageTime = datetime.fromisoformat(message["messageTime"])
        userMessage = message["userMessage"]
        userName = message["userName"]
        print(f"Пользователь \"{userName}\" отправлял сообщение \"{userMessage}\" {messageTime.strftime('%Y-%m-%d %H:%M:%S')}")
    sleep(5)
