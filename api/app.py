# from api import create_app

# app = create_app()
# cli.register(app)

import json
import awsgi
from flask import (
    Flask,
    jsonify,
)

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(status=200, message='OK')


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    '''
    print("Received event: " + json.dumps(event, indent=2))

    response = {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        }
    }

    response['body'] = """<html>
    <head>
    <title>Swiss Pair</title>
    <style>
    html, body {
    margin: 0; padding: 0;
    font-family: arial; font-weight: 700; font-size: 2em;
    text-align: center;
    }
    </style>
    </head>
    <body>
    <p>Swiss Pair. Coming Soon.</p>
    </body>
    </html>"""

    return response
