# Harmony Node Stats

## vStatsBot Alerts
- This is an automated script that will periodically ( every 30 mins ) send your node data to vStats for dashboard + alerts.
- Each alert can be turned on and off on a node by node basis ( via config.py ) or globally via /notifications on vStatsBot.

### Dashboard:

Shows your node stats on a single page.

Unique page can be found by running /nodestats in vStatsBot

Example dashboard https://vstats.one/node-stats/example

### Alerts:

Node summary request. Type /nodestats for a server summary. These are also scheduled daily. 

All of the below can be toggled on or off via the config.py file.

- <b>Blockchain Sync - Compares local vs remote height</b>
```
🔻Shard2-Hel --- Shard 0 Behind🔻
Remote: 22716160
Local: 22711441
Difference: -4719
```
- <b>Space Left - Alerts you when space is lower than 30GB</b>
```
🔻Shard2-fsn --- Space Low 20GB Left🔻
```
- <b>If your node has gone into 'Syncing' mode due to a harmony error, it will alert you.</b>
```
🚨!!! shard3-fsn = Syncing !!!🚨
Please check node.
```
- <b>Daily Node Summary Updates</b>
```
🔶Shard3🔶
Shard 3: Normal | Synced
Load: 0.73 | 0.74 | 0.72
Space: 119G
Updated: 14 mins ago
```

## Data Collected
- Harmony Utility Metadata
- Blockchain Height ( Remote + Local )
- Hostname
- Server Load
- Server Space in current filesystem

## Pre Installation Notes
- Script must be installed on each individual node

## Installation 

### Download the script
We suggest storing it in your home folder.

```
cd ~/
git clone https://github.com/FortuneV13/harmony_node_stats
cd harmony_node_stats
```
To update use `git pull`


## Automatic Installation:
```python3 install.py```
A special thanks to Patrick (Easy Node Validator) for supplying this script to help speed up the installation process. 

## Manual Installation:
### Get a token
Send the command `/token` to the @vStatsBot on telegram to get your token.

Copy the token, as message on telegram will auto delete after 60 seconds.

The same token can be used on all your nodes. 

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
