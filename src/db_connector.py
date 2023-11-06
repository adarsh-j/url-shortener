#!/usr/local/bin/python3

import logging
import os
import psycopg2
import sys
import time

_log = logging.getLogger(__name__)

class DbConnector():
    def __init__(self, short_url_len):
        self.short_url_len = short_url_len

        self._get_conn()
        _log.info('Successfully connected to the database')

        self.cursor = self.conn.cursor()
        self._create_tables()

    def _get_conn(self):
        conn_str = os.getenv('CONNECTION')
        max_retries = 10

        for i in range(max_retries):
            try:
                self.conn = psycopg2.connect(conn_str)
                self.conn.autocommit = True
                return
            except Exception as e:
                _log.error(f'Cannot connect to the database: {e}')
                time.sleep(1)
        sys.exit(1)

    def _create_tables(self):
        create_urls_table = f"""CREATE TABLE IF NOT EXISTS urls (
                    short_url VARCHAR PRIMARY KEY,
                    long_url VARCHAR NOT NULL,
                    total_count bigint DEFAULT 0,
                    constraint short_url CHECK(length(short_url)={self.short_url_len})
                );
            """

        try:
            self.cursor.execute(create_urls_table)
        except Exception as e:
            _log.error(f'Cannot create urls table: {e}')
            sys.exit(1)

        create_metrics_table = """CREATE TABLE IF NOT EXISTS metrics (
                    time TIMESTAMPTZ NOT NULL,
                    short_url VARCHAR(7),
                    FOREIGN KEY (short_url) REFERENCES urls (short_url)
                );
            """
        try:
            self.cursor.execute(create_metrics_table)
        except Exception as e:
            _log.error(f'Cannot create metrics table: {e}')
            sys.exit(1)

        create_metrics_hypertable = "SELECT create_hypertable('metrics', 'time', if_not_exists => TRUE);"
        try:
            self.cursor.execute(create_metrics_hypertable)
        except Exception as e:
            _log.error(f'Cannot create metrics hypertable: {e}')
            sys.exit(1)

        data_retention_policy = "SELECT add_retention_policy('metrics', INTERVAL '7 days', if_not_exists => TRUE);"
        try:
            self.cursor.execute(data_retention_policy)
        except Exception as e:
            _log.error(f'Cannot create data retention policy: {e}')
            sys.exit(1)

    def insertUrl(self, shortUrl, longUrl):

        query = f"INSERT INTO urls (short_url, long_url) VALUES ('{shortUrl}', '{longUrl}')"

        try:
            self.cursor.execute(query)
        except Exception as e:
            _log.error(f"Failed to insert into urls shorturl:{shortUrl}, longurl:{longUrl}, {e}")
            raise(e)

    def getLongUrl(self, shortUrl):
        query = f"SELECT * FROM urls where short_url='{shortUrl}'"

        try:
            self.cursor.execute(query)
        except Exception as e:
            _log.error(e)
        row = self.cursor.fetchall()

        if len(row) == 0:
            return None
        elif len(row) > 1:
            _log.error(f'More than 1 long_urls returned for {shortUrl}')
        return row[0][1]

    def purgeUrl(self, shortUrl):
        query = f"DELETE FROM urls where short_url='{shortUrl}'"
        self.cursor.execute(query)

    def insertMetric(self, shortUrl, time):
        query = f"INSERT INTO metrics (time, short_url) VALUES (to_timestamp({time}), '{shortUrl}');"
        self.cursor.execute(query)

    def incrTotalAccessCount(self, shortUrl):
        query = f"UPDATE urls SET total_count = total_count + 1 WHERE short_url='{shortUrl}';"
        self.cursor.execute(query)

    def getTotalAccessCount(self, shortUrl):
        query = f"SELECT * FROM urls where short_url='{shortUrl}';"
        self.cursor.execute(query)
        row = self.cursor.fetchall()

        if len(row) == 0:
            return None
        elif len(row) > 1:
            _log.error(f'More than 1 long_urls returned for {shortUrl}')
        return row[0][2]

    def getHourlyAccessCount(self, shortUrl, start_time, end_time):
        query = f"select count(time) from metrics where short_url='{shortUrl}' and time>=to_timestamp({start_time}) and time<=to_timestamp({end_time});"
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        if len(row) == 0:
            return 0
        return row[0][0]

    def purgeMetrics(self, shortUrl):
        query = f"DELETE FROM metrics where short_url='{shortUrl}';"
        self.cursor.execute(query)

