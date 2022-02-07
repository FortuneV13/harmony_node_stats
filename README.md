# Node Stats

# vStats Alerts
This is an automated script that will periodically send your node to vStats to enable easy to view and compare stats.


### 1) Download the script
We suggest storing it in your home folder.

```
cd ~/
git clone https://github.com/DavidWhicker/harmony_node_stats.git
cd harmony_node_stats
```
To update use `git pull`

### 2) Get a token
Send the command `/token` to the @vStatsBot on telegram to get your token.

Copy the token, as message on telegram will auto delete after 60 seconds.

### 3) Setup 
Install required packages if missing:

<!-- `sudo apt update && sudo apt upgrade -y` -->
```
sudo apt install python3-pip
pip3 install -r requirements.txt
```
Rename .env.example to .env and edit the following variables:
```
cp .env.example .env
nano .env
```
> VSTATS_TOKEN="" Add your token from vstats 

> DOUBLE_SIGN_CHECK_ENABLED=true|false (Default: false - Will alert you if a blskey match is found on 1 or more servers )

> SYNC_CHECK_ENABLED=true|false (Default: false  Will alert when local vs remote gap is larger than 100 )

> SPACE_CHECK_ENABLED=true|false (Default: false  Will alert when space is less than 25GB )

> HARMONY_FOLDER="" (Add path containing .hmy. Run pwd in .hmy location to get full path e.g /home/serviceharmony/harmony )

### 4) Test Script 
Test the .env variables and script is working as expected. 

Run the below from the script directory:

```
python3 main.py
```

Alerts on screen AND vStatsBot should appear. Once successful, please cancel the script ( CTRL + C ) and move onto the next step.

### 5) Setup Service
Now setup script to run as a service in the background. 

Run the following with root privileges. If you do not have access with root then you may setup a tmux session ( see: Alternative Setup - Tmux ).

Please note: add correct info for < USER > & < PATH TO SCRIPT >

```
cat<<-EOF > /etc/systemd/system/harmony_node_stats.service
[Unit]
Description=harmony_node_stats daemon
After=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=<USER>
WorkingDirectory=<PATH TO SCRIPT>
ExecStart=python3 main.py
SyslogIdentifier=harmony_node_stats
StartLimitInterval=0
LimitNOFILE=65536
LimitNPROC=65536

[Install]
WantedBy=multi-user.target
EOF
```
Followed by:

```
sudo systemctl daemon-reload
sudo chmod 755 /etc/systemd/system/harmony_node_stats.service
sudo systemctl enable harmony_node_stats.service
sudo service harmony_node_stats start
sudo service harmony_node_stats status
```

### 5b) Alternative Setup - Tmux

`tmux new-session -s harmony_node_stats`

`cd ~/harmony_node_stats/`

`python3 main.py`


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

Status Check
```
sudo service harmony_node_stats status
```
