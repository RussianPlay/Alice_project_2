from flask import Flask, request
import logging
import json
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

translator_url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
headers = {
    'x-rapidapi-key': "286a48c82cmsh83930d71ba2fb4ap124a57jsndefca9bce98d",
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
}
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    if not req["session"]["new"]:
        text = req["request"]["command"].split("слово")[-1].strip()
        querystring = {"langpair": "ru|en",
                       "q": text,
                       "mt": "1",
                       "onlyprivate": "0",
                       "de": "ahmadullinta@mail.ru",
                       "format": "json"}
        response = requests.request("GET", translator_url, headers=headers, params=querystring)
        res["response"]["text"] = response.json()["responseData"]["translatedText"]
    else:
        res["response"]["text"] = "| Welcome to translator! |"


if __name__ == '__main__':
    app.run()


