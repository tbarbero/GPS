#!/usr/bin/python
from ftplib import FTP
import os, os.path
from datetime import datetime, date, timedelta
import time

# Create a script that will artifiically create a time delay (subtract some amount of time from current day) then run this script at 24:00, so it will see the previous days files and pull the 23-hr file. We can subtract timedeltas (some amount of time) from datetime objects.
# This script will be run at 00:00 of every day by crontab



# Get current day UTC time
currentday = datetime.utcnow()

# Create a time delay variable
tdelta = timedelta(days=1)

# Note here: it is important to subtract one day from the datetime object rather than just index backwards one day in the string converted datetime object because if the current day is 05-01-2020, and we index the string converted object backwards we will set the date as 05-00-2020 which is not a valid date. By subtracting one day from the datetime object, it will return another datetime object that is 04-30-2020, which our goal.

# Create a variable for previous day
previousday = str(currentday-tdelta)

# Concatenates the year and month into one variable
tyearmonth = previousday[0:4] + previousday[5:7]

# Creates a day variable
tday = previousday[8:10]

#tyearmonth and tday are now variables that will return currentday - 1 day (yesterday) so we are able to CD into yesterdays directories and pull the 23-hr file and store it in yesterday's directory when this script runs at 00:00 of everyday (the new day)

# Logging into server
ftp = FTP('server_IP_Address')
print('Attempting login into Evan Research Lab GPS...')
ftp.login('username', 'password')
print('Login successful.')

# Starting time
start = time.time()

# Go into yesterday's directory
ftp.cwd('/Internal/'+tyearmonth+'/'+tday)


#ftp.nlst() is a method that returns all of the files in current working directory. There are other types of files in this such as .RINEX .obs etc..., we only want the raw data (.T02 files) so we loop through the list of files and if the file type is .T02, we concatenate the .T02 file to the end of our tfiles list.
# Get the list of .T02 files of yesterday
tfiles=[]
filelist = ftp.nlst()
for element in range(0,len(filelist)):
    abc = filelist[element][43:56]
    if abc[9:13] == '.T02':
        tfiles.append(abc)

# Moving around local directories. This section of code creates directories for each month and each day to store the files in. If they are already created, then just CD into that month or day.
os.chdir('/data/SaltonSea/GPS')
try:
    os.mkdir(tyearmonth)
except:pass
os.chdir(tyearmonth)
try:
    os.mkdir(tday)
except:pass
os.chdir(tday)

# Set a counter for how much data is being used to download files.
counter = 0

# Loop through the .T02 files. If the file already exists locally (we already downloaded previously hourly files), skip over this file and only download new files. Other parts of code include some metadata: fs = file size (to see how much data is being used), counter = accumulates how much data is used to download files, time.time() = timer to see how long file download takes.
# open(tfiles[qwerty], "wb+") is a line of code that opens a text file locally.
# ftp.retrbinary('RETR '+ tfiles[qwerty], file.write) then opens the .T02 in the GPS and copies the .T02 raw data (which is in binary) to the local file in the server. Then it does this with all the .T02 files in that day's directory. Essentially this is the same as downloading the .T02 files from the GPS to the server.
# Downloading files
for qwerty in range(0,len(tfiles)):
    if os.path.isfile(tfiles[qwerty]):
        print(tfiles[qwerty],'exists, skipping over')
    else:
        print('Copying', tfiles[qwerty], 'to local directory')
        fs = ftp.size(tfiles[qwerty])
        counter = counter + fs
        file = open(tfiles[qwerty], "wb+")
        ftp.retrbinary('RETR '+ tfiles[qwerty], file.write)
        file.close()
        
# Displaying some metadata
kcounter = counter/1000
mcounter = float(counter/1e6)
end = time.time()
elapsed = end - start
print('Downloaded ', kcounter, ' kB | ', mcounter, ' mB')
print('Time elapsed: ', elapsed, 'seconds')
print('Leaving Evan-Lab-GPS...')
ftp.quit()
