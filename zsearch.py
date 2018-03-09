#!/usr/bin/python3

import logging
import requests
import configparser
import sys
import re
import json
import time

class ZSearch:
    'ZoomEye searcher'

    def __init__(self, is_internal = False, output_name = ""):
        self.logger = logging.getLogger("ZSearch")
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.logger.addHandler(self.log_handler)
        self.formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        self.log_handler.setFormatter(self.formatter)


        self.config = configparser.ConfigParser()
        self.load_config()
        self.is_internal = is_internal
        self.session = requests.session()
        self.output_file = "result/z_%s_%s.txt" % (output_name, time.strftime('%Y_%m_%d_%H_%M_%S'))

    def load_config(self):
        self.logger.info("Load configure.")
        try:
            self.config.read('config.ini')
        except:
            self.logger.critical("Config file error, rename config.ini.sample and edit it.")
            sys.exit(1)

    def login(self):
        if self.is_internal:
            # internal zoomeye can show chinese IP address
            self.logger.info("Logging into internal zoomeye.")
            data = {
                'username': self.config['internal']['username'],
                'password': self.config['internal']['password']
            }
            res = self.session.post(self.config['internal']['login_url'], data = data)
            if res.status_code != 200:
                self.logger.error("Login failed. Check your config.")
                sys.exit(1)
            else:
                reg = re.compile(r"localStorage\.token=\"(.*?)\";")
                self.token = re.search(reg, res.text).group(1)
                self.logger.info("Login success.")
        else:
            self.logger.error('external is under develop')
            sys.exit(0)

    def search(self, dork, page):
        if self.is_internal:
            # search with internal zoomeye
            headers = {
                'Cube-Authorization' : self.token
            }
            data = {
                'q' : dork,
                'p' : page
            }
            res = self.session.get(self.config['internal']['api_url'],
                headers = headers, params = data)
            result = json.loads(res.text)['matches']
            self.logger.debug("Returned %d results." % len(result))
            return result
        else:
            self.logger.error('external is under develop')
            sys.exit(0)

    def write(self, result):
        with open(self.output_file, 'a') as fp:
            for item in result:
                if 'site' in item:
                    # if result is a domain name, it will possibly have multi-ip
                    host = item['site']
                else:
                    host = item['ip']
                
                # domain name results have no port
                if 'portinfo' in item:
                    wstr = "%s:%s\n" % (host, item['portinfo']['port'])
                else:
                    wstr = "%s\n" % host
                fp.write(wstr)

