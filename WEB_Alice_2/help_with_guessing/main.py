from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

cities = {
    'москва': ['937455/0d92a3a245fdcc16c646',
               '1652229/0fe8c15ac45a09a47aef'],
    'нью-йорк': ['1521359/fd431a1f89556c431caa',
                 '1652229/4d443f83ff9edef075b6'],
    'париж': ["937455/29f2b5e040304267157c",
              '937455/1f6341b8073e13a01258']
}
sessionStorage = {}


@app.route("/post", methods=["POST"])
def main():
    logging.info(f"Request: {request.json!r}")
    response = {
        "session": request.json["session"],
        "version": request.json["version"],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f"Response: {response!r}")
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req["session"]["user_id"]

    if req["session"]["new"]:
        res["response"]["text"] = "Привет! Назови свое имя!"
        sessionStorage[user_id] = {
            "first_name": None
        }
        return

    if sessionStorage[user_id]["first_name"] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res["response"]["text"] = "Не расслышала имя. Повтори, пожалуйста!"
        else:
            sessionStorage[user_id]["first_name"] = first_name
            res["response"]["text"] = \
                "Приятно познакомиться, " + first_name.title() + "Алиса. Какой город хочешь увидеть?"
    else:
        if req["request"]["command"].lower() == "помощь":
            res["response"]["text"] = "Ты просто должен написать название города и я ее угадаю"
        else:
            city = get_city(req)
            if city in cities:
                res["response"]["card"] = {}
                res["response"]["card"]["type"] = "BigImage"
                res["response"]["card"]["title"] = "Этот город я знаю."
                res["response"]["card"]["image_id"] = random.choice(cities[city])
                res["response"]["text"] = "Я угадал"
            else:
                res["response"]["text"] = "Первый раз слышу об этом городе. Попробуй еще разок!"
    res["response"]["buttons"] = [{
        "title": city.title(),
        "hide": True
    } for city in cities] + [{"title": "Помощь",
                              "hide": True}]


def get_city(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.GEO":
            return entity["value"].get("city", None)


def get_first_name(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.FIO":
            return entity["value"].get("first_name", None)


if __name__ == "__main__":
    app.run()
