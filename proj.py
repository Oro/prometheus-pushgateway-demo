#!/usr/bin/env python3

import argparse
import requests
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

#Argument parsing
parser = argparse.ArgumentParser(description='Process a list of URLs and writes the result to Prometheus.', fromfile_prefix_chars='@')
parser.add_argument('-t', '--timeout', default=5, type=float, help='timeout in seconds (default: 5)')
parser.add_argument('-p', '--pushgateway', metavar='URL', type=str, help='pushgateway endpoint, if ommited will only output the result to stdout.')
parser.add_argument('urls', metavar='URL', type=str, nargs ='+', help='URL to check. Can also be supplied in a newline separated file via @file')
args = parser.parse_args()

#Initialize prom gateway metric
registry = CollectorRegistry()
c = Gauge('promgatewaydemo_http_request_last_run_unixtime', 'Last time the promgateway demo was executed', ['http_status', 'url', 'exception'], registry=registry)

for url in args.urls:
    try:
        response = requests.head(url, timeout=args.timeout)
    except requests.exceptions.RequestException as err:
        print(url, err)
        if args.pushgateway:
            # Push the exception name as label to prometheus
            c.labels(exception=type(err).__name__, url=url, http_status='').set_to_current_time()
        continue
    print(url, response)
    if args.pushgateway:
        c.labels(http_status=response.status_code, url=url, exception='').set_to_current_time()

#After all urls are looped through, push metric if pushgateway is supplied via args
if args.pushgateway:
    push_to_gateway(args.pushgateway, job='promgateway_demo', registry=registry)
