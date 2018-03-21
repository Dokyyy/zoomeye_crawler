#!/usr/bin/python3
from zsearch import ZSearch
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--external', action = 'store_true', help = 'use external zoomeye?')
    parser.add_argument('-d', '--dork', required = True, help = 'dork text')
    parser.add_argument('-p', '--pages', required = True, type = int, help = 'max page to get')
    parser.add_argument('-f', '--filename', help = 'output file name')
    parser.add_argument('-h', '--host', action = 'store_true', help = 'search for device only(t=host)')    
    args = parser.parse_args()

    z = ZSearch(not args.external, args.filename)
    z.login()
    count = 0
    for page in range(1, args.pages + 1):
        z.logger.info("Getting page %d of %d" % (page, args.pages))
        result = z.search(args.dork, page, args.host)
        if len(result) > 0:
            count += len(result)
            z.write(result)
        else:
            z.logger.info("No more result.")
            break
        if page % 60 == 0:
            z.logger.warning("Take a 30s rest...")            
            time.sleep(30)
    z.logger.info("%s results in total." % count)

    
        
    
    