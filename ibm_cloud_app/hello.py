from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import cf_deployment_tracker
import json
import requests

# Emit Bluemix deployment event
cf_deployment_tracker.track()
# must needed by Bluemix setting
port = int(os.getenv('PORT', 8000))

app = Flask(__name__)

@app.route('/vreco/<img>', methods=['GET'])
def visualReco(img):
    # call visual-recognition webapi
    url = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=befb491ae8c532e1db72518f6da8088bb2bd1b52&url=https://namickey.github.io/ai_train_2018/img/'+img+'&version=2016-05-20'
    headers = {'Accept-Language': 'ja'}
    tmpResponse = requests.get(url, headers=headers)

    # allow-origin
    newJsonResponse = jsonify(tmpResponse.json())
    newJsonResponse.headers.add('Access-Control-Allow-Origin', '*')
    return newJsonResponse

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
