# app_settings.py
import datetime
import os

now = datetime.datetime.now()
date = str(now.year) + '-' + str(now.month)+'-'+ str(now.day)
print(date)

mongoPath = 'mongodb://localhost:27017/'
jwtSecret = 'super-secret'
logfile = 'logfile.log'
#logfile =  date + 'logfile.log'