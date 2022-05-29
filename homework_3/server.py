import random
from datetime import datetime
from typing import List

import flask
from flask import Flask, jsonify, Response


class MessageModel:
    '''
    Модель для обмена данными между сервисами
    '''
    userName: str
    userMessage: str
    messageTime: datetime

    def __init__(self, userName: str, userMessage: str, messageTime: datetime):
        self.userName = userName
        self.userMessage = userMessage
        self.messageTime = messageTime

    def __json__(self):
        '''
        Преваращает обьект в json
        :return: обьект в json формате
        '''
        return {
            "userName": f"{self.userName}",
            "userMessage": f"{self.userMessage}",
            "messageTime": f"{self.messageTime}"
        }


def get_response_message(message: str) -> Response:
    '''
    Утилитная функция для формирования сообщения ответа
    :param message: Входящее сообщение
    :return: сообщение в json формате
    '''
    responseMessage = jsonify({"message": str(message)})
    responseMessage.headers["Content-Type"] = "application/json"
    return responseMessage


app = Flask(__name__)
database: List[MessageModel] = []


@app.route("/sendMessage", methods=['POST'])
def send_message():
    '''
    Функция для отправки нового сообщения пользователем
    :return: Статус об отправке сообщения
    '''

    availableUserNameKey = "userName"
    availableUserMessageKey = "userMessage"
    keysErrorMessage = f"Доступные параметры ключей: {availableUserNameKey}, {availableUserMessageKey}"

    userDataAsDict = flask.request.json  # получить json из запроса и положить его в словарь
    print("Пользователь ввел данные: ", userDataAsDict)

    if not isinstance(userDataAsDict, dict):
        return get_response_message("Передаваемые параметры должны быть в формате Json"), 400

    if len(userDataAsDict) > 2:
        return get_response_message(f"Доступное количество параметров: 2\n{keysErrorMessage}"), 400

    if availableUserNameKey not in userDataAsDict or availableUserMessageKey not in userDataAsDict:
        return get_response_message(f"Параметры ключей не соответствуеют доступным.\n{keysErrorMessage}"), 400

    userName = userDataAsDict[availableUserNameKey]
    userMessage = userDataAsDict[availableUserMessageKey]

    if not isinstance(userName, str):
        return get_response_message(f"Параметр {availableUserNameKey} должен иметь строковый формат"), 400
    if len(userName) == 0:
        return get_response_message(f"Параметр {availableUserNameKey} не должен быть пустым"), 400
    if not userName.isalpha():
        return get_response_message(f"Параметр {availableUserNameKey} должен состоять только из букв"), 400
    if not isinstance(userMessage, str):
        return get_response_message(f"Параметр {availableUserMessageKey} должен иметь строковый формат"), 400
    if len(userMessage) == 0:
        return get_response_message(f"Параметр {availableUserMessageKey} не должен быть пустым"), 400

    if userMessage[:5] == '/anon':  # если сообщение начинается со слова anon, то оно должно быть анонимным
        anonymousMsgModel = MessageModel(userName="Аноним", userMessage=userMessage[6:],
                                         messageTime=datetime.now())
        database.append(anonymousMsgModel)
    else:
        msgModel = MessageModel(userName=userName, userMessage=userMessage, messageTime=datetime.now())
        database.append(msgModel)

    availableBotCommands = {'/help', '/cat', '/coin'}
    if userMessage in availableBotCommands:
        answerMessage = MessageModel(userName="Бот", userMessage=None, messageTime=datetime.now())
        if userMessage == '/help':
            msg = "/help - вывести список доступных команд\n" \
                  "/cat - нарисовать котика\n" \
                  "/coin - подбросить монетку\n" \
                  "/anon -- отправить анонимное сообщение"
            answerMessage.userMessage = msg
        elif userMessage == '/cat':
            msg = ''' /\_/\ ♥\n >^,^<\n  / \ \n (   )'''
            answerMessage.userMessage = msg
        elif userMessage == '/coin':
            if random.randint(0, 1):
                msg = "Орёл"
                answerMessage.userMessage = msg
            else:
                msg = "Решка"
                answerMessage.userMessage = msg
        database.append(answerMessage)
    return get_response_message("Сообщение успешно отправлено"), 200


@app.route("/messages", methods=['GET'])
def get_messages():
    '''
    Функуция для получения сообщений.
    Принимает дату ISO формата 2022-05-29 00:30:39.697739
    :return: Список всех пользователей и сообщений отправленных пользователями
    '''
    availableDateKey = "afterDate"
    keysErrorMessage = f"Доступные параметры ключей: {availableDateKey}"

    userDataAsDict = flask.request.json  # получить json из запроса и положить его в словарь
    print("Пользователь ввел данные: ", userDataAsDict)

    if not isinstance(userDataAsDict, dict):
        return get_response_message("Передаваемые параметры должны быть в формате Json"), 400

    if len(userDataAsDict) > 1:
        return get_response_message(f"Доступное количество параметров: 1\n{keysErrorMessage}"), 400

    if availableDateKey not in userDataAsDict:
        return get_response_message(f"Параметры ключей не соответствуеют доступным.\n{keysErrorMessage}"), 400

    dateAfter = userDataAsDict[availableDateKey]
    if not isinstance(dateAfter, str):
        return get_response_message(f"Параметр {availableDateKey} должен иметь строковый формат"), 400

    try:
        dateAsIsoDateTime = datetime.fromisoformat(dateAfter)
    except ValueError:
        return get_response_message(f"Не удалось получить дату из передаваемого параметра {availableDateKey}"), 400

    resultList = []
    for message in database:
        if message.messageTime > dateAsIsoDateTime:
            resultList.append(message.__json__())

    responseMessage = jsonify({"messages": resultList})
    responseMessage.headers["Content-Type"] = "application/json"

    return responseMessage, 200


@app.route("/status", methods=['GET'])
def print_status():
    '''
    Функция для проверки общего статуса по БД
    :return: Информацию о пользователях и сообщениях на текущий момент
    '''
    # берем только уникальных пользователей
    uniqueUsers = set()
    for messageModel in database:
        uniqueUsers.add(messageModel.userName)

    usersCount = len(uniqueUsers)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    messagesCount = len(database)

    responseMessage = jsonify({"status": str("OK"), "timestamp": str(timestamp), "usersCount": str(usersCount),
                               "messagesCount": str(messagesCount), "users": list(uniqueUsers)})
    responseMessage.headers["Content-Type"] = "application/json"
    return responseMessage, 200


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
