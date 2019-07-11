#!/usr/bin/env python

import sys

from botocore.exceptions import ClientError

from orgcrawler import orgs, crawlers, utils
from orgcrawler.cli.utils import setup_crawler

#cycles = 2
cycles = 100 
errors = 0
role = sys.argv[1]
timer = crawlers.CrawlerTimer()
cycle_timer = crawlers.CrawlerTimer()
master_account_id = utils.get_master_account_id(role)

timer.start()
for i in range(cycles):
    cycle_timer.start()
    try:
        org = orgs.Org(master_account_id, role)
        org.load()
    except ClientError as e:
        errors += 1
        print(e)
    org.clear_cache()
    org = None 
    cycle_timer.stop()
    print('cycle: {}\ttime: {}'.format(i, cycle_timer.elapsed_time))
timer.stop()

print('cycles:', cycles)
print('errors:', errors)
print('elapsed time:', timer.elapsed_time)
print('average time:', timer.elapsed_time / cycles)


