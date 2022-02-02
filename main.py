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

alerts = Alerts(VSTATS_API, connect_to_api, **alerts_context)

while True:
    try:
        node_stats = getNodeStats()
        shard = node_stats['shard-id']
        
        remote_shard_0 = [f'{envs.HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers', '--node=https://api.s0.t.hmny.io']
        result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
        remote_shard = [f'{envs.HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers', f'--node=https://api.s{shard}.t.hmny.io']
        result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        remote_data_shard = json.loads(result_remote_shard.stdout)
        local_shard = [f'{envs.HARMONY_FOLDER}/hmy', 'blockchain', 'latest-headers']
        result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        local_data_shard = json.loads(result_local_shard.stdout)
        
        send_shard_0_remote =  literal_eval(local_data_shard['result']['beacon-chain-header']['number'])
        send_shard_0_local =  literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])
        send_shard_main_remote =  literal_eval(local_data_shard['result']['shard-chain-header']['number'])
        send_shard_main_local =  literal_eval(remote_data_shard['result']['shard-chain-header']['number'])
        
        alerts.send_data(node_stats, send_shard_0_remote, send_shard_0_local, send_shard_main_remote, send_shard_main_local)
        
    except Exception as e:
        alerts.generic_error(e)
        log.error(e)
        log.error(f"Please fix me!")

    # Delay by x seconds
    #sleep(envs.RUN_EVERY_X_MINUTES * 60)
    sleep(60)
    # Hot reload Env
    envs.load_envs()