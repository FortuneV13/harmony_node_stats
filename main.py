import json
import subprocess
import os

from time import sleep
from includes.config import *
from util.connect import connect_to_api
from util.tools import *
from util.send_alerts import Alerts
from subprocess import Popen, PIPE, run
from ast import literal_eval

# Init Alerts Class
alerts = Alerts(VSTATS_API, connect_to_api, **alerts_context)

# Keep Looping
while True:

    # Set default node heights
    send_shard_0_remote = 0
    send_shard_0_local = 0
    send_shard_main_remote = 0
    send_shard_main_local = 0
    
    try:
        # Get Node utility metadata
        node_stats = getNodekStats()
        
        # Get Shard ID from node
        shard = node_stats['shard-id']
        
        # Shard 0 - Remote
        result_shard_0_remote = run([f'{envs.HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s0.t.hmny.io'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        result_shard_0_remote = json.loads(result_shard_0_remote.stdout)
        send_shard_0_remote =  literal_eval(result_shard_0_remote['result']['shard-chain-header']['number'])
        
        # Shard Main - Remote
        result_shard_main_remote = run([f'{envs.HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{shard}.t.hmny.io'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        result_shard_main_remote = json.loads(result_shard_main_remote.stdout)
        send_shard_main_remote =  literal_eval(result_shard_main_remote['result']['shard-chain-header']['number'])
        
        # Locals
        result_local_shard = run([f'{envs.HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        result_local_shard = json.loads(result_local_shard.stdout)
        # Shard 0 - Local
        send_shard_0_local =  literal_eval(result_local_shard['result']['beacon-chain-header']['number'])
        # Shard Main - Local
        send_shard_main_local =  literal_eval(result_local_shard['result']['shard-chain-header']['number'])
  
        # Get Server Load
        load = os.getloadavg()

        # Send to vStats
        alerts.send_data(node_stats, send_shard_0_remote, send_shard_0_local, send_shard_main_remote, send_shard_main_local, load)
        
    except Exception as e:
        #alerts.generic_error(e)
        log.error(e) 
        log.error(f"Please fix me!")

    # Delay by x seconds
    #sleep(envs.RUN_EVERY_X_MINUTES * 60)
    sleep(30*60)
    # Hot reload Env
    envs.load_envs()