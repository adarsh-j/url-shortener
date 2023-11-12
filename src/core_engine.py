#!/usr/local/bin/python3

import logging
import random
import string
import time
from db_connector import DbConnector

_log = logging.getLogger(__name__)

class UrlEngine:
    def __init__(self):
        self.short_url_len = 6
        self.char_pool = [ c for c in string.ascii_lowercase ]
        self.char_pool.extend([ c for c in string.ascii_uppercase ])
        self.char_pool.extend([ c for c in string.digits ])
        
        self.db = DbConnector(self.short_url_len)

    def _generateShortUrl(self):
        shortUrl = ''
        for i in range(self.short_url_len):
            r = random.randrange(len(self.char_pool))            
            shortUrl += self.char_pool[r]
        return shortUrl

    def getLongUrl(self, shortUrl, incr=False):
        longUrl = self.db.getLongUrl(shortUrl)

        _log.info(longUrl)
        _log.info(shortUrl)
        if longUrl and incr:
            self.db.incrTotalAccessCount(shortUrl)
            self.db.insertMetric(shortUrl, int(time.time()))
        return longUrl

    def createShortUrl(self, longUrl):
        shortUrl = self._generateShortUrl()
        self.db.insertUrl(shortUrl, longUrl)
        return shortUrl

    def deleteShortUrl(self, shortUrl):
        # Also purge the metrics associated with this shortUrl
        self.db.purgeMetrics(shortUrl)
        self.db.purgeUrl(shortUrl)

    def getMetrics(self, shortUrl, start_time, end_time):
        if start_time == 0:
            count = self.db.getTotalAccessCount(shortUrl)
        else:
            count = self.db.getHourlyAccessCount(shortUrl, start_time, end_time)
        return count
