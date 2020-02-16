#!/usr/bin/env python
# coding: utf-8

# In[1]:


def gps_download_all(localdir, server, user, password):

    """
    gps_download_all(localdir=, server=, user=, password=)
    
        Function for FTPing into GPS and downloading ALL .T02 raw files
        
        Formating for GPS files
        -----------------------
        Path Style: YYYYMM/DD
        Name Style: YYMMDDHH
        *Suominet requires 30 second intervals for files
        
        Parameters (strings)
        --------------------
        localdir: /local/path/of/where/data/will/be/stored
        server: static IP address of Trimble GPS
        user: username to login to GPS
        password: password to login to GPS
               
        Returns
        -------
        .T02 files in organized directories of all .T02 files in GPS
        
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
    
    # starting timer
    start = time.time()
    
    # FTP into GPS
    ftp = FTP(server)
    print('Attempting login into Evan Research Lab GPS...')
    ftp.login(user, password)
    print('Login successful.')
    
    # getting list of months    
    m = ftp.nlst()
    mons = [m[i][43:49] for i in range(0,len(m))]
    months = []
    for a in range(0,len(mons)):
        if mons[a][0:2] == '20':
            months.append(mons[a])
        
    # changing directory into each month directory
    for month in months:
        ftp.cwd('/Internal')
        print('CD into ', month)
        ftp.cwd(month)
        
        # getting list of days
        d = ftp.nlst()
        days = [d[c][43:49] for c in range(0,len(d))]
        for day in days:
            ftp.cwd('/Internal/'+month)
            print('CD into ', day)
            
            # changing directory into each day
            ftp.cwd(day)
            
            # getting list of .T02 files
            f = ftp.nlst()
            files = [f[e][43:56] for e in range(0,len(f))]
            t02files = []
            for g in range(0,len(files)):
                if files[g][9:13] == '.T02':
                    t02files.append(files[g])
                    
            # creating respective local directories for .T02 files
            for fi in range(0,len(t02files)):
                os.chdir(localdir)
                try:
                    os.mkdir(month)
                except:pass
                os.chdir(month)
                try:
                    os.mkdir(day)
                except:pass
                os.chdir(day)
            
                # downloading files
                counter = 0
                localfile = os.path.join(localdir,month,day,t02files[fi])
                if os.path.isfile(t02files[fi]):
                    print(t02files[fi], 'exists, skipping over...')
                else:
                    print('Copying ', t02files[fi])
                    fs = ftp.size(t02files[fi])
                    counter = counter + fs
                    file = open(t02files[fi], "wb+")
                    ftp.retrbinary('RETR '+ t02files[fi], file.write)
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
    print('Leaving FTP-GPS session...')

