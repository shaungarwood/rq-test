#!/usr/bin/env python3.7

from IPython import embed

from redis import Redis
from rq import Queue
from rq.job import Job
from time import sleep

from stats import pull_stats

def whatever():
    sleep(1)
    return("whatever")

redis = Redis(host="192.168.200.5")
q = Queue(connection=redis)

failed = q.failed_job_registry
#failed_jobs = failed.get_job_ids()
#whatever = Job.fetch(failed_jobs[0], connection=redis)
#whatever.exc_info

job = q.enqueue(sleep, 5)
embed()

while True:
    if job.is_failed:
        print("job ", job.id, " failed")
        job.refresh()
        print(job.exc_info)
        exit(1)
    elif job.is_finished:
        print("job ", job.id, " finished with result: ", job.result)
        exit(0)
    else:
        print("job hasn't finished yet")
        sleep(1)
