#!/usr/local/bin/python3

import logging
import random
import string

_log = logging.getLogger(__name__)

class UrlEngine:
    def __init__(self):
        self.short_url_len = 6
        self.char_pool = [ c for c in string.ascii_lowercase ]
        self.char_pool.extend([ c for c in string.ascii_uppercase ])
        self.char_pool.extend([ c for c in string.digits ])
        
    def _generateShortUrl(self):
        shortUrl = ''
        for i in range(self.short_url_len):
            r = random.randrange(len(self.char_pool))            
            shortUrl += self.char_pool[r]
        return shortUrl

    def getLongUrl(self, shortUrl, incr=False):
        return "longUrl"

    def createShortUrl(self, longUrl):
        shortUrl = self._generateShortUrl()
        return shortUrl

    def deleteShortUrl(self, shortUrl):
        return

    def getMetrics(self, shortUrl, start_time, end_time):
        return 0
