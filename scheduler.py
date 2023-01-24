from hash_model import updateAll
import datetime

todays_date = datetime.date.today()

if todays_date.day == 5 or todays_date.day == 15 or todays_date.day == 25:
    updateAll()