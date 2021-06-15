import asyncio
import websockets
import json
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
import requests


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"   # =)
jwt = JWTManager(app)


def analyze(jsn_data):
    """
    Производится анализ подписи запроса
    :param jsn_data: Данные в формате JSON вида {name:"имя отправителя", message:"сообщение"}
    :return: bool
    """
    try:
        data = json.loads(jsn_data)
        mess = data["message"].split(' ')
        if mess[0] == "auth":
            res = requests.post('localhost:5000/protected', data={"Authorization": f"{data['name']} {mess[0]}"})
            res = res.json()
            return True if res["name"] == data["name"] else False
    except Exception as exp:
        print(exp)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Получение имени пользователя из токена
    :return:
    """
    current_user = get_jwt_identity()
    return jsonify(name=current_user), 200



async def messages(websocket, _):
    """
    Функция "слушает" ws-порт и отвечает на запросы, приходящие на этот порт.
    :return: None
    """
    user_mess = await websocket.recv()

    answer = "Ok"
    # TODO формирование ответа
    await websocket.send(answer)


start_server = websockets.serve(messages, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

