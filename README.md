# Harmony Node Stats

## vStatsBot Alerts
- This is an automated script that will periodically ( every 30 mins ) check your node for errors e.g out of sync and alert you via vStatsBot.
- Each alert can be turned on and off via /notifications on vStatsBot.

### Alert Examples:

The following are automatic if a problem is detected:

- <b>Blockchain Sync - Compares local vs remote height</b>
```
🔻Shard3 Node --- Shard 0 Behind🔻
Remote: 22716160
Local: 22711441
Difference: -4719
```
- <b>Space Left - Alerts you when space is lower than 30GB</b>
```
🔻Shard3 Node --- Space Low 20GB Left🔻
```
- <b>If your node has gone into 'Syncing' mode due to a harmony error, it will alert you.</b>
```
🚨!!! Shard3 Node = Syncing !!!🚨
Please check node.
```
- <b>Daily Node Summary Updates - These are scheduled twice daily and on command via /nodestats</b>
```
🔶Shard3 Node🔶
Shard 3: Normal | Synced
Load: 0.73 | 0.74 | 0.72
Space: 119G
Updated: 14 mins ago
```

## Pre Installation Notes
- Script must be installed on each individual node
- Each server must have a unique hostname/servername.

## Get a token
Send the command `/token` to the @vStatsBot on telegram to get your token.

Copy the token, as message on telegram will auto delete after 120 seconds.

The same token can be used on all your nodes. 

## Automatic Installation:
If you are using custom ports or harmony cli is stored in a folder other than base or harmony folder then please move to 'Manual Installation'
```
python3 install.py
```
You will need to obtain a token from vStatsBot using the /token command on the bot. The installation script will ask for this token. 

Once complete you should get a ping from vStatsBot to know it installed correctly.

A special thanks to Patrick (Easy Node Validator) for supplying this install script to help speed up the installation process. 

## Manual Installation:
### Download the script 
```
cd ~/ && git clone https://github.com/FortuneV13/harmony_node_stats && cd harmony_node_stats
```

### Setup 
Install required packages if missing:

<!-- `sudo apt update && sudo apt upgrade -y` -->
```
sudo apt install python3-pip
pip3 install -r requirements.txt
```
Rename config.example.py to config.py and edit the following variables:
```
cp config.example.py config.py
```

Edit config.py variables ( now support for multiple shards per server):
```
#Add your token from vstats. Run /token on vStatsBot
VSTATS_TOKEN="" 

# Add path containing .hmy. Run pwd in .hmy location to get full path e.g /home/serviceharmony/harmony 
SHARD_ARRAY = {
	
	"first-shard":{
		"harmony_folder":"/home/serviceharmony/harmony",
		"node_port":9501,
	},
	
	# "second-shard":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501,
	# },
	
	# "third-shard":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501,
	# },
	
    # "forth-shard":{
	# 	"harmony_folder":"/home/serviceharmony/harmony",
	# 	"http_port":9501,
	# },
	
}
```
### Test Script 
Test the config variables and script is working as expected. 

Run the below from the script directory:

```
python3 main.py
```

Alerts on screen AND vStatsBot should appear. Once successful, please cancel the script ( CTRL + C ) and move onto the next step.

## Automate the script via a service 
Now setup script to run as a service in the background. 

Run the following with sudo privileges. 
```
sudo vi /etc/systemd/system/harmony_node_stats.service
```
Copy the below into the service file making sure to edit the User and WorkingDirectory first. 
```
[Unit]
Description=harmony_node_stats daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=serviceharmony
WorkingDirectory=/home/serviceharmony/harmony_node_stats
ExecStart=python3 main.py
SyslogIdentifier=harmony_node_stats
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
```
Type `:wq` to save and exit. 

Now enable the service:

```
sudo systemctl daemon-reload
sudo chmod 755 /etc/systemd/system/harmony_node_stats.service
sudo systemctl enable harmony_node_stats.service
sudo service harmony_node_stats start
sudo service harmony_node_stats status
```

### Logs
Check logs to make sure the script is running as expected. 

### Misc
Start Service
```
sudo service harmony_node_stats start
```

Stop Service
```
sudo service harmony_node_stats stop
```
Restart Service
```
sudo service harmony_node_stats restart
```

Status Check
```
sudo service harmony_node_stats status
```
