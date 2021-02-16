import settings_transfer as ST
from pexpect import *
import getpass
import re
import os

regex = re.compile('\\w+\\r')
os.system("ssh-keyscan -H "+ST.HOST+" >> "+ST.PATH_SSH+" > /dev/null 2>&1")

#Copy all new files of Apps
def Apps():
    print("Copying Apps")
    cmd_apps = "/usr/bin/rsync --rsync-path='sudo rsync' -avzh "+ST.USER+"@"+ST.HOST+":"+ST.REMOTE_DIR_APPS+" "+ST.LOCAL_DIR_APPS+""
    run(cmd_apps, timeout=3600, events={"Active Directory password":""+ST.PASSWD+"\r"})
    
#Copy all new files of Modinputs
def Modinputs():
    print("Copying Modinputs")
    cmd_apps = "/usr/bin/rsync --rsync-path='sudo rsync' -avzh "+ST.USER+"@"+ST.HOST+":"+ST.REMOTE_DIR_MODINPUTS+" "+ST.LOCAL_DIR_MODINPUTS+""
    run(cmd_apps, timeout=3600, events={"Active Directory password":""+ST.PASSWD+"\r"})

#Copy the files generated in KVStore in the last 24 hours
def KVStore():
    print("Copying Last KVstore Files")
    login = "ssh "+ST.USER+"@"+ST.HOST+" 'sudo find "+ST.REMOTE_DIR_KVSTORE+" -mtime 1 -type f -printf '%f,''"
    (command_output)=run(login,events={"Active Directory password": "" + ST.PASSWD + "\r"})
    command=str(command_output).split('Active Directory password:')[-1]
    files=command.replace('\r\n','').replace(',',' ').rstrip()
    list=files.split(' ')
    i=0
    while i<len(list):
        #print('transfering')
        cmd_kvstore = "/usr/bin/rsync --rsync-path='sudo rsync' -avzh " + ST.USER + "@" + ST.HOST + ":" + ST.REMOTE_DIR_KVSTORE + "/"+list[i]+" " + ST.LOCAL_DIR_KVSTORE + ""
        run(cmd_kvstore, events={"Active Directory password": "" + ST.PASSWD + "\r"})
        i+=1

#Clean files older than 7 days
def Clean():
    print("Cleaning Old KVStore Files ")
    loginclean = "ssh "+ST.USER+"@"+ST.HOST+" 'sudo find "+ST.REMOTE_DIR_KVSTORE+" -mtime +7 -type f -printf '%f,''"
    (command_output)=run(loginclean,events={"Active Directory password": "" + ST.PASSWD+ "\r"})
    command=str(command_output).split('Active Directory password:')[-1]
    files=command.replace('\r\n','').replace(',',' ').rstrip()
    listclean=files.split(' ')
    i=0
    while i<len(listclean):
        #print('excluding')
        #print(listclean[i])
        clean = "ssh "+ST.USER+"@"+ST.HOST+" 'rm " + ST.REMOTE_DIR_KVSTORE +"/"+listclean[i]+''
        run(clean, events={"Active Directory password": "" + ST.PASSWD + "\r"})
        i+=1

#Modules Activation
print("Starting DR process")
Apps()
Modinputs()
KVStore()
#Clean()

print("Done")
