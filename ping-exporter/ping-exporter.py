#!/usr/bin/env python3

import asyncio
import time
import datetime
from ping3 import ping
from prometheus_client import start_http_server, Counter, Histogram


prefix="ping"
port=9400
buckets=(.00025, .0005, .001, .002, .004, .008, .016, .032, .064, .128, .256, 0.512, 1.024, 10)
pings = Histogram(f"{prefix}", "Ping responses",['target'], buckets=buckets)
lost = Counter(f"{prefix}_lost", "Pings lost", ['target'])
unresolved = Counter(f"{prefix}_unresolved", "Pings that could not resolve address", ['target'])

start_http_server(port)

targets = ['gate-sw.grootland', 'nettest.arlut.utexas.edu',
    'unifi.grootland', 'gate-manager.groot-iot']

for t in targets:
    unresolved.labels(t)
    lost.labels(t)
    pings.labels(t)

while True:
    for target in targets:
        rc = ping(target)
        if rc is None:
            lost.labels(target).inc()
        elif rc is False:
            unresolved.labels(target).inc()
        else:
            pings.labels(target).observe(rc)

    time.sleep(1)
