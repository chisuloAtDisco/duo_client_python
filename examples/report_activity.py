#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import sys
import csv
import duo_client
from six.moves import input

argv_iter = iter(sys.argv[1:])
def get_next_arg(prompt):
    try:
        return next(argv_iter)
    except StopIteration:
        return input(prompt)

# Configuration and information about objects to create.
admin_api = duo_client.Admin(
    ikey=get_next_arg('Admin API integration key ("DI..."): '),
    skey=get_next_arg('integration secret key: '),
    host=get_next_arg('API hostname ("api-....duosecurity.com"): '),
)

next_offset = None
limit = '100'
sort = 'ts:desc'
mintime = get_next_arg('Mintime: ')
maxtime = get_next_arg('Maxtime: ')
limit_arg = get_next_arg('Limit (Default = 100, Max = 1000): ')
if limit_arg:
    limit = limit_arg
next_offset_arg = get_next_arg('Next_offset: ')
if next_offset_arg:
    next_offset = next_offset_arg

sort_arg = get_next_arg('Sort (Default - ts:desc) :')
if sort_arg:
    sort = sort_arg

reporter = csv.writer(sys.stdout)
logs = admin_api.get_activity_logs(mintime = mintime, maxtime = maxtime, limit = limit, next_offset = next_offset, sort = sort)

reporter.writerow(('activity_id', 'ts', 'action', 'actor_name', 'target_name'))
for log in logs['items']:
    activity = log['activity_id'],
    ts = log['ts']
    action = log['action']
    actor_name = log.get('actor', {}).get('name', None)
    target_name = log.get('target', {}).get('name', None)
    reporter.writerow([
        activity,
        ts,
        action,
        actor_name,
        target_name,
    ])