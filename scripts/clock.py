from apscheduler.schedulers.blocking import BlockingScheduler


import os

import PushToPerm
import connection
import updatePrices
import calculateMargins
import time



#changed BackgroundScheduler to BlockingScheduler
#scheduler = BlockingScheduler(timezone="Iceland")
scheduler = BlockingScheduler()
from rq import Queue
from rq.job import Job
from worker import conn

q=Queue(connection=conn)


#'''
@scheduler.scheduled_job('cron', hour='0,2,4,6,8,10,12,14,16,18,20,22')
def clock_scheduled_commands():
    print('Updating Tables')
    job = q.enqueue_call(func=updatePrices.main, timeout='6m')
    print('Updating Margins')
    job = q.enqueue_call(func=calculateMargins.main, timeout='6m')
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#'''
'''
@scheduler.scheduled_job('interval', minutes=5)
def timed_job():
    #con = connection.establish_connection()
    print('Updating Tables')
    job = q.enqueue_call(func=updatePrices.main, timeout='6m')
    print(job.get_id())
    print('Calculating Margins')
    job = q.enqueue_call(func=calculateMargins.main, timeout='6m')
    print(job.get_id())
    #print('Pushing to Perm')
    #PushToPerm.main()
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    #con.close()
    return 0
'''
'''
scheduler.add_job(
    func=print_date_time, # your function here
    trigger=IntervalTrigger(minutes=1),
    id='doingsmth_job',
    name='Update tables and recalculate profit margins every 6 hours',
    replace_existing=True)
'''
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

