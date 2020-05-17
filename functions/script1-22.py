#!/usr/bin/python
from ftplib import FTP
import os, os.path
from datetime import datetime, date
import time

# Converting to UTC from PST
heure = str(datetime.utcnow())
tyearmonth = heure[0:4] + heure[5:7]
tday = heure[8:10]

# Logging into server
ftp = FTP('Server-IP-Address')
print('Attempting login into Evan Research Lab GPS...')
ftp.login('username', 'password')
print('Login successful.')

# Starting time
start = time.time()

# Go into todays directory
ftp.cwd('/Internal/'+tyearmonth+'/'+tday)
#ftp.cwd('/Internal/202005/04')

# Get the list of .T02 files of current day
tfiles=[]
locallist = ftp.nlst()
for element in range(0,len(locallist)):
    abc = locallist[element][43:56]
    if abc[9:13] == '.T02':
        tfiles.append(abc)    

# Moving around local directories
os.chdir('/data/SaltonSea/GPS')
try:
    os.mkdir(tyearmonth)
except:pass
os.chdir(tyearmonth)
try:
    os.mkdir(tday)
except:pass
os.chdir(tday)

counter = 0
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
kcounter = counter/1000
mcounter = float(counter/1e6)
end = time.time()
elapsed = end - start
print('Downloaded ', kcounter, ' kB | ', mcounter, ' mB')
print('Time elapsed: ', elapsed, 'seconds')
print('Leaving Evan-Lab-GPS...')
ftp.quit()
