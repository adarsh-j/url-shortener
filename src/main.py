#!/usr/local/bin/python3

import logging
from flask import Flask

from routes import route_blueprint

_log = logging.getLogger(__name__)

app = Flask('UrlShortener')
app.register_blueprint(route_blueprint)


if __name__ == '__main__':
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    app.run(host='0.0.0.0', port=8000)

