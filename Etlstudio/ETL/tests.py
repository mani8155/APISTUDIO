import schedule
import time

def job():
    print("Job is running...")

# Schedule job to run every 10 minutes
schedule.every(10).minutes.do(job)

# Schedule job to run every hour
schedule.every().hour.at(":44").do(job)

# Schedule job to run daily at 10:30 AM
schedule.every().day.at("10:30").do(job)


# schedule.every().week.do(job)

# Schedule job to run weekly on Monday at 10:30 AM
schedule.every().saturday.at("10:40").do(job)

# while 0:
#     schedule.run_pending()
#     time.sleep(1)
