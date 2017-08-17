from apscheduler.schedulers.blocking import BlockingScheduler
import calculateMargins
import updatePrices
import PushToPerm
import time
import connection


#changed BackgroundScheduler to BlockingScheduler
scheduler = BlockingScheduler(timezone="Iceland")

#'''
@scheduler.scheduled_job('cron', hour='0,3,6,9,12,15,18')
def clock_scheduled_commands():
    print('Updating Tables')
    updatePrices.main(connection)
    print('Updating Margins')
    calculateMargins.main()
    #print('Pushing to Perm')
    #PushToPerm.main()
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#'''
'''
@scheduler.scheduled_job('interval', minutes = 6)
def timed_job():
    print('Updating Tables')
    updatePrices.main()
    print('Updating Margins')
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

