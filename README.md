# Step 1: install python3
```
sudo su
sudo apt-get update
sudo apt-get install python3.7
sudo apt-get install python3-pip
```
# Step 2: Config the config.ini file

```
[SCHEDULE]
;support integer 
number = 3 
;support minute, hour, day
by = second
_>>> it will run 1 time per / 3 seconds
[EACH]
;number of packet default = 10000
packet = 10000
->> scan 10000 req each time
```
# Step 3: Run
```
git clone https://github.com/pnngnas/ydcc-app.git
pip install -r requirement.txt
python3 py.py &
```
