#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def gps_download(tyearmonth, tday, localdir, server, user, password):
    
    """
    gps_download(tyearmonth=, tday=, localdir=, server=, user=, password=)
    
        Function for FTPing into GPS and downloading .T02 raw files from Trimble NetR9
        
        Formating for GPS files
        -----------------------
        Path Style: YYYYMM/DD
        Name Style: YYMMDDHH
        *** suominet requires 30 second intervals for files
        
        Parameters (strings)
        --------------------
        tyearmonth: YYYYMM
        tday: DD 
        *** if desired day is current day, enter the None datatype for tyearmonth and tday
        localdir: /local/path/of/where/data/will/be/stored
        server: static IP address of Trimble GPS
        user: username to login to GPS
        password: password to login to GPS
               
        Returns
        -------
        .T02 files in organized directories located in specific local path
        
        
        Libraries necessary to run function
        -----------------------------------
        from ftplib import FTP
        import os, os.path
        from datetime import datetime, date
        import time 
    """
    
    # import libraries
    from ftplib import FTP
    import os, os.path
    from datetime import datetime, date
    import time

    # FTP into GPS
    ftp = FTP(server)
    print('Attempting login into Evan Research Lab GPS...')
    ftp.login(user, password)
    print('Login successful.')
    
    # default date as current day
    if (tyearmonth and tday) == None:
        heure = str(datetime.utcnow())
        tyearmonth = heure[0:4] + heure[5:7]
        tday = heure[8:10]
    
    # starting timer
    start = time.time()
    
    # change into current directory
    ftp.cwd('/Internal/'+tyearmonth+'/'+tday)
    
    # gets the list of .T02 files of tday
    tfiles=[]
    lst = ftp.nlst()
    for e in range(0,len(lst)):
        f = lst[e][43:56]
        if f[9:13] == '.T02':
            tfiles.append(f)       

    # creating and moving around local directories
    os.chdir(localdir)
    try:
        os.mkdir(tyearmonth)
    except:pass
    os.chdir(tyearmonth)
    try:
        os.mkdir(tday)
    except:pass
    os.chdir(tday)
    
    # starting byte counter
    counter = 0
    
    # downloading files
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

    # display metadata
    kcounter = counter/1000
    mcounter = float(counter/1e6)
    end = time.time()
    elapsed = end - start
    print('Downloaded ', kcounter, ' kB | ', mcounter, ' mB')
    print('Time elapsed: ', elapsed, 'seconds')
    print('Leaving Evan-Lab-GPS...')
    ftp.quit()

