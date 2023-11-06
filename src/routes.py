#!/usr/local/bin/python3

import logging
from flask import (Blueprint,
                    jsonify,
                    make_response,
                    abort,
                    redirect,
                    request
                    )
import time

from core_engine import UrlEngine

_log = logging.getLogger(__name__)

route_blueprint = Blueprint('route_bleuprint', __name__)
urlEngine = UrlEngine()

@route_blueprint.route('/')
def index():
    resp = dict()
    resp['msg'] = 'Welcome to URL Shortener service'
    return make_response(jsonify(resp))

@route_blueprint.route('/<shorturl>')
def readUrl(shorturl):
    if len(shorturl) != urlEngine.short_url_len:
        return abort(make_response(jsonify(message="Page does not exist"), 404))

    try:
        longUrl = urlEngine.getLongUrl(shorturl, incr=True)
    except Exception as e:
        logging.exception(e)
        return abort(make_response(jsonify(message="Page does not exist"), 404))

    if not longUrl:
        return abort(make_response(jsonify(message="Page does not exist"), 404))
    return redirect(longUrl, code=302) 

@route_blueprint.route('/api/v1/create', methods=['POST'])
def createUrl():
    resp = dict()
   
    try:
        longUrl = request.json.get('url')
    except Exception as e:
        logging.error(f'Failed to extract url, {e}')
        return abort(make_response(jsonify(message="A URL is required to create a shortened alias to it"), 404))

    resp['longurl'] = longUrl

    try:
        shortUrl = urlEngine.createShortUrl(longUrl)
    except Exception as e:
        logging.exception(e)
        resp['shorturl'] = None
        return make_response(jsonify(resp), 500)
   
    resp['shorturl'] = shortUrl
    return make_response(jsonify(resp))

@route_blueprint.route('/api/v1/delete', methods=['DELETE'])
def deleteUrl():
    resp = dict()

    try:
        shortUrl = request.json.get('shorturl')
    except Exception as e:
        logging.error(f'Failed to extract shorturl, {e}')
        return abort(make_response(jsonify(message="Specify the short url to be deleted"), 404))
        
    resp['shorturl'] = shortUrl

    try:
        urlEngine.deleteShortUrl(shortUrl)
    except Exception as e:
        logging.exception(e)
        return make_response(jsonify(resp), 500)

    resp['message'] = "Successfully deleted"
    return make_response(jsonify(resp))

@route_blueprint.route('/api/v1/metrics/<shorturl>/<hour>')
def getMetrics(shorturl, hour):
    resp = dict()
    resp['shorturl'] = shorturl

    end_time = int(time.time())
    if hour == 0:
        start_time = 0
    else:
        start_time = end_time - (hour * 60 * 60)

    try:
        count = urlEngine.getMetrics(shorturl, start_time, end_time)
    except Exception as e:
        logging.error(f'Failed to get metrics for shorturl:{shorturl}, {e}')
        return abort(make_response(jsonify(message="Specify the short url"), 404))

    resp['count'] = count
    resp['start_time'] = start_time
    resp['end_time'] = end_time
    return make_response(jsonify(resp))

