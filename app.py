#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    with open('data.json') as data_file:
        data = json.load(data_file)
    
    if req.get("result").get("action") == "stockrate":
        name = req.get("result").get("parameters").get("name")
        day = req.get("result").get("parameters").get("day")
        if name == "IBM":
            if day == "today":
                return data["users"]["today"]["IBM"]
            if day == "yesterday":
                return data["users"]["yesterday"]["IBM"]
            if day == "all":
                return data["users"]["all"]["IBM"]
            return data["sorry"]
        if name == "walmart":
            if day == "today":
                return data["users"]["today"]["walmart"]
            if day == "yesterday":
                return data["users"]["yesterday"]["walmart"]
            if day == "all":
                return data["users"]["all"]["walmart"]
            return data["sorry"]
        if name == "ford":
            if day == "today":
                return data["users"]["today"]["ford"]
            if day == "yesterday":
                return data["users"]["yesterday"]["ford"]
            if day == "all":
                return data["users"]["all"]["ford"]
            return data["sorry"]
    if req.get("result").get("action") == "userdata":
        return data["userdata"]
    return data["sorry"]

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
