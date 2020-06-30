#!/usr/bin/env python

import argparse
import requests
from prometheus_client import CollectorRegistry, Counter, push_to_gateway

#Argument parsing
parser = argparse.ArgumentParser(description='Process a list of URLs and writes the result to Prometheus.')
parser.add_argument('-t', '--timeout', default=5, type=float, help='timeout in seconds (default: 5)')
parser.add_argument('-p', '--pushgateway', metavar='URL', type=str, help='pushgateway endpoint, if ommited will only output the result to stdout.')
parser.add_argument('urls', metavar='URL', type=str, nargs ='+', help='URL to check')
args = parser.parse_args()

#Initialize prom gateway metric
registry = CollectorRegistry()
c = Counter('urlcheck_http_request_count', 'HTTP requests and their corresponding responses', ['http_status', 'url'], registry=registry)

for url in args.urls:
    response = requests.head(url, timeout=args.timeout)
    print(url, response)
    if args.pushgateway:
        c.labels(http_status=response.status_code, url=url).inc()

#After all urls are looped through, push metric if pushgateway is supplied via args
if args.pushgateway:
    push_to_gateway(args.pushgateway, job='urlcheck', registry=registry)
