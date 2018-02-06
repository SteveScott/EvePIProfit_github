from apscheduler.schedulers.blocking import BlockingScheduler


import os

import PushToPerm
import connection
import updatePrices
import calculateMargins
import time



#changed BackgroundScheduler to BlockingScheduler
scheduler = BlockingScheduler(timezone="Iceland")

'''
@scheduler.scheduled_job('cron', hour='0,2,4,6,8,10,12,14,16,18,20,22')
def clock_scheduled_commands():
    con = connection.establish_connection()
    print('Updating Tables')
    updatePrices.main()
    print('Updating Margins')
    main()
    #print('Pushing to Perm')
    #PushToPerm.main()
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    con.close()
'''
'''
@scheduler.scheduled_job('interval', minutes = 6)
def timed_job():
    print('Updating Tables')
    updatePrices.main()
    print('Calculating Margins')
    calculateMargins.main()
    #print('Pushing to Perm')
    #PushToPerm.main()
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
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

