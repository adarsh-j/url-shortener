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
    """
    This endpoint serves the home page
    """
    resp = dict()
    resp['msg'] = 'Welcome to URL Shortener service'
    return make_response(jsonify(resp))

@route_blueprint.route('/<shorturl>')
def readUrl(shortUrl):
    """
    This endpoint is used to redirect (HTTP code 302) the short URL to the actual long URL.
    If the short URL does not exist, a HTTP code 404 is returned.
    All short URLs are 6 character length and contain [a-zA-Z0-9] characters only.
    """
    if len(shortUrl) != urlEngine.shortUrlLen:
        return abort(make_response(jsonify(message="Page does not exist"), 404))

    try:
        longUrl = urlEngine.getLongUrl(shortUrl, incr=True)
    except Exception as e:
        _log.error(f"Failed to get longUrl for shortUrl:{shortUrl}, {e}")
        return abort(make_response(jsonify(message="Page does not exist"), 404))

    if not longUrl:
        return abort(make_response(jsonify(message="Page does not exist"), 404))
    return redirect(longUrl, code=302) 

@route_blueprint.route('/api/v1/create', methods=['POST'])
def createUrl():
    """
    This endpoint is used to create a short URL from a real URL.
    The short URL returned is unique and points to this original URL only.
    Accepts the `url` in JSON format.
    Example Input:
    ```
    {
        "url" : "www.google.com"
    }
    ```
    Example Output:
    ```
    {
        "longurl" : "www.google.com",
        "shorturl" : "X8uE9s"
    }
    ```
    """
    try:
        longUrl = request.json.get('url')
    except Exception as e:
        _log.error(f'Failed to extract url, {e}')
        return abort(make_response(jsonify(message="A URL is required to create a shortened alias to it"), 404))

    resp = dict()
    resp['longurl'] = longUrl

    try:
        shortUrl = urlEngine.createShortUrl(longUrl)
    except Exception as e:
        _log.exception(f"Failed to create shortUrl:{longUrl}, {e}")
        resp['message'] = "Failed to create short url"
        return make_response(jsonify(resp), 500)
   
    resp['shorturl'] = shortUrl
    return make_response(jsonify(resp))

@route_blueprint.route('/api/v1/delete', methods=['DELETE'])
def deleteUrl():
    """
    This endpoint is used to delete an existing short URL and all its associated metrics.
    A HTTP code 404 is returned if the short URL does not exist.
    Example Input:
    ```
    {
        "url" : "x8uE9s"
    }
    ```
    Example Output:
    ```
    {
        "message" : "success",
        "shorturl" : "X8uE9s"
    }
    ```
    """
    resp = dict()

    try:
        shortUrl = request.json.get('url')
    except Exception as e:
        _log.error(f'Failed to get shortUrl:{shortUrl}, {e}')
        return abort(make_response(jsonify(message="Specify the short url to be deleted"), 404))
        
    resp['shorturl'] = shortUrl

    try:
        urlEngine.deleteShortUrl(shortUrl)
    except Exception as e:
        _log.error(f"Failed to delete shortUrl:{shortUrl}, {e}")
        return make_response(jsonify(resp), 500)

    resp['message'] = "success"
    return make_response(jsonify(resp))

@route_blueprint.route('/api/v1/metrics/<shorturl>/<hour>')
def getMetrics(shorturl, hour):
    """
    This endpoint is used to get the number of times a specific short URL was accessed,
    in the number of hours specified.
    hour is an integer between 0 and 168 (which is the number of hours in a week).
    If the hour is 0, all time access count is returned. Otherwise, access time is the past
    <hour> hours is returned.

    A HTTP code 404 is returned if
        - The short URL does not exist.
        - Hour is not an integer between 0 and 168.
    Success return is a JSON which contains
        - short URL
        - count, in int
        - start_time, which is (current time) - (number of hours) in epoch seconds OR
            0 if hour is 0
        - end_time, which is (current time) in epoch seconds

    Example Input:
    ```
    /api/v1/metrics/x8uE9s/24
    ```
    Example Output:
    ```
    {
        "shorturl" : "X8uE9s"
        "count" : 128,
        "start_time" : "1699422878",
        "end_time" : "1699426478"
    }
    ```
    """
    resp = dict()
    resp['shorturl'] = shorturl
    try:
        hour = int(hour)
    except Exception as e:
        _log.error(f'Failed to extract hour, {e}')
        return abort(make_response(jsonify(message="Specify the number of hours in integer"), 404))

    if int(hour) > ( 7 * 24):
        return abort(make_response(jsonify(message="Hourly metrics up to a week are stored."), 404))

    end_time = int(time.time())
    if hour == 0:
        start_time = 0
    else:
        start_time = end_time - (hour * 60 * 60)

    try:
        count = urlEngine.getMetrics(shorturl, start_time, end_time)
    except Exception as e:
        _log.error(f'Failed to get metrics for shorturl:{shorturl}, {e}')
        return abort(make_response(jsonify(message="Specify the short url"), 404))

    resp['count'] = count
    resp['start_time'] = start_time
    resp['end_time'] = end_time
    return make_response(jsonify(resp))

