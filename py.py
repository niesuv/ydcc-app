import os, signal
import configparser
import schedule
import subprocess
import time
import requests
from datetime import datetime


def doreq(filename):
    url = "35.240.246.167:8000/"

    payload = {}
    files=[
    ('file',('syn.pcap',open(filename,'rb'),'application/octet-stream'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    with open("history.txt" , '+a') as file:
        file.write("\n" + response.text)
    

lastpid = -1
lasttime = 0
config = configparser.ConfigParser()
config.read("config.ini")
def job():
    global lastpid
    try:
        if lastpid != -1:
            os.kill(lastpid, signal.SIGTERM)
        datenow = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        statement = ['tcpdump', '-i', 'any' ,'-nn', '-c' , str(packet) , '-w' ,datenow + '.pcap'] 
        process =  subprocess.Popen(statement, shell=True)
        lastpid = process.pid
        if lasttime != 0:
            doreq(datenow + ".pcap")    
            

        
    except ProcessLookupError:
        pass
    except PermissionError:
        pass    
    except OSError:
        datenow = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        statement = ['tcpdump', '-i', 'any' ,'-nn', '-c' , str(packet) , '-w' ,datenow + '.pcap'] 
        statement = ['dir']
        process =  subprocess.Popen(statement, shell=True)
        lastpid = process.pid
        if lasttime != 0:
            doreq(datenow + ".pcap") 

number = 1
by = 'day'
packet = 1000
if 'SCHEDULE' in config and "number" in config['SCHEDULE']:
    number = int(config["SCHEDULE"]["number"])

if 'SCHEDULE' in config and "by" in config['SCHEDULE']:
    by = config["SCHEDULE"]["by"]

if 'EACH' in config and "packet" in config['EACH']:
    packet = int(config["EACH"]["packet"])


if by == 'day':
    schedule.every(number).days.do(job)
if by == 'hour':
    schedule.every(number).hours.do(job)
if by == 'minute':
    schedule.every(number).minutes.do(job)
if by == 'second':
    schedule.every(number).seconds.do(job)



while True:
    schedule.run_pending()
    time.sleep(1)






