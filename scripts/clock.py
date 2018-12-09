from apscheduler.schedulers.blocking import BlockingScheduler


import os
import atexit
import PushToPerm
import connection
import updatePrices
import calculateMargins
import time



#changed BackgroundScheduler to BlockingScheduler
#scheduler = BlockingScheduler(timezone="UTC")
scheduler = BlockingScheduler()
from rq import Queue
from rq.job import Job
from worker import conn

q=Queue(connection=conn)

'''
@scheduler.scheduled_job('interval', minutes=30)
def clock_scheduled_commands():
    print('Updating Tables')
    job = q.enqueue_call(func=updatePrices.main, timeout='10m')
    print('Updating Margins')
    job = q.enqueue_call(func=calculateMargins.main, timeout='10m')
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
'''
'''
@scheduler.scheduled_job('cron', hour='0,4,8,12,16,20')
def clock_scheduled_commands():
    print('Updating Tables')
    job = q.enqueue_call(func=updatePrices.main, timeout='10m')
    print('Updating Margins')
    job = q.enqueue_call(func=calculateMargins.main, timeout='10m')
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
'''
#'''
@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    #con = connection.establish_connection()
    print('Updating Tables')
    job = q.enqueue_call(func=updatePrices.main, timeout='10m')
    print(job.get_id())
    print('Calculating Margins')
    job = q.enqueue_call(func=calculateMargins.main, timeout='10m')
    print(job.get_id())
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    #con.close()
    return 0
#'''

scheduler.start()
atexit.register(lambda: scheduler.shutdown())

