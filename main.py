import subprocess
import os
from time import sleep
from includes.config import *
from util.connect import connect_to_api
from util.tools import *
from bases.alerts import Alerts
from subprocess import Popen, PIPE, run,check_output
from ast import literal_eval

# Init Alerts Class
alerts = Alerts(VSTATS_API, connect_to_api, **alerts_context)

# Init Count 
count = 0

# Keep Looping
while True:
    # increment count
    count = count + 1
    # Set defaults
    load = None
    send_shard_0_remote = None
    send_shard_0_local = None
    send_shard_main_remote = None
    send_shard_main_local = None
   
        
    try:
        # Get Server Load
        try:
            load = os.getloadavg()
        except Exception as e:
            load = None
        
        # Get Node utility metadata
        node_stats = getNodeStats()
        # Get Shard ID from node
        shard = node_stats['shard-id']
        
        try:
            # Shard 0 - Remote
            result_shard_0_remote = getSyncRemote(f'https://api.s0.t.hmny.io')
            send_shard_0_remote =  literal_eval(result_shard_0_remote['shard-chain-header']['number'])
            # Shard Main - Remote
            result_shard_main_remote = getSyncRemote(f'https://api.s{shard}.t.hmny.io')
            send_shard_main_remote =  literal_eval(result_shard_main_remote['shard-chain-header']['number'])
            # Locals
            result_local_shard = getSyncLocal()
            send_shard_0_local =  literal_eval(result_local_shard['beacon-chain-header']['number'])
            send_shard_main_local =  literal_eval(result_local_shard['shard-chain-header']['number'])
        except Exception as e:
            send_shard_0_remote = None
            send_shard_0_local = None
            send_shard_main_remote = None
            send_shard_main_local = None
            
        try:
            # Space left
            space = subprocess.check_output('df -BG --output=avail "$PWD" | tail -n 1', shell=True).decode(sys.stdout.encoding)
        except Exception as e:
            space = None
            
        # # Send to vStats
        alerts.send_to_vstats(node_stats, send_shard_0_remote, send_shard_0_local, send_shard_main_remote, send_shard_main_local, load,space,count)
        
    except Exception as e:
        log.error(e) 
        log.error(f"Please fix me!")
        alerts.generic_error(e)
        

    # Delay by x seconds
    #sleep(envs.RUN_EVERY_X_MINUTES * 60)
    sleep(30*60)
    # Hot reload Env
    envs.load_envs()
