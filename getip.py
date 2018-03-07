#!/usr/bin/python3
from zsearch import ZSearch
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', required = True, help = 'dork text')
    parser.add_argument('-p', required = True, type = int, help = 'max page to get')
    parser.add_argument('-f', help = 'output file name')
    args = parser.parse_args()

    z = ZSearch(True, args.f)
    z.login()
    for page in range(1, args.p):
        z.logger.info("Getting page %d of %d" % (page, args.p))
        result = z.search(args.d, page)
        if len(result) > 0:
            z.write(result)
        else:
            z.logger.info("No more result.")
            break

    
        
    
    