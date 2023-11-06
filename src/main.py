#!/usr/local/bin/python3

from flask import Flask


app = Flask('UrlShortener')

@app.route('/')
def index():
    resp = dict()
    resp['msg'] = 'Welcome to URL Shortener service'
    return make_response(jsonify(resp))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
