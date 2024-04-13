import os, signal
import configparser
import schedule
import subprocess
import time
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini")
def job():
    try:
        os.kill(lastpid, signal.SIGTERM)
        datenow = datenow.now().strftime(r"%Y-%m-%d %H:%M:%S")
        statement = ['tcpdump', '-i', 'any' ,'-nn', '-c' , str(packet) , '-w' ,datenow + '.pcap']
        process =  subprocess.Popen(statement)
        lastpid = process.pid
        
    except ProcessLookupError:
        pass
    except PermissionError:
        pass    

number = 1
by = 'day'
packet = 1000
if 'SCHEDULE' in config and "number" in config['SCHEDULE']:
    number = int(config["SCHEDULE"]["number"])

if 'SCHEDULE' in config and "by" in config['SCHEDULE']:
    by = config["SCHEDULE"]["by"]

if 'EACH' in config and "packet" in config['EACH']:
    packet = int(config["EACH"]["packet"])


lastpid = -1
if by == 'day':
    schedule.every(number).days.do(job)
if by == 'hour':
    schedule.every(number).hours.do(job)
if by == 'minute':
    schedule.every(number).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)






