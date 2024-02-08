import subprocess
import os
from time import sleep
from includes.setup import *
from api.connection import alerts
from includes.tools import *
from subprocess import Popen, PIPE, run,check_output
from ast import literal_eval
from config import *

# Init Count 
count = 0

# Keep Looping
while True:
    # increment count
    count = count + 1
    
    try:
        # Get Server Load
        try:
            load = os.getloadavg()
        except Exception as e:
            load = None
        
        try:
            # Space left
            space = subprocess.check_output('df -BG --output=avail "$PWD" | tail -n 1', shell=True).decode(sys.stdout.encoding)
        except Exception as e:
            space = None
            
        if SHARD_ARRAY:
            for shardKey, shardValue in SHARD_ARRAY.items():
                # Set defaults
                block_remote = None
                block_local = None
                # Get Node utility metadata
                node_stats = getNodeStats(shardValue)
                if node_stats is not None:
                    # Get data from metadata to pass to vstats
                    shard = node_stats['shard-id']
                    blskey = node_stats['blskey']
                    peerid = node_stats['peerid']
                    sigingMode = node_stats['consensus']['mode']
                    # Get block heights
                    try:
                        remote_api_array = getSyncRemote(shardValue,f'https://api.s{shard}.t.hmny.io')
                        block_remote =  literal_eval(remote_api_array['shard-chain-header']['number'])
                        
                        local_api_array = getSyncLocal(shardValue)
                        if(shard == 0):
                            block_local =  literal_eval(local_api_array['beacon-chain-header']['number'])
                        else:
                            block_local =  literal_eval(local_api_array['shard-chain-header']['number'])
                        
                    except Exception as e:
                        block_remote = None
                        block_local = None

                    # Send to vStats
                    alerts.send_to_vstats(shardKey,blskey,peerid,sigingMode,shard, block_remote, block_local, load,space,count)
        
        
    except Exception as e:
        log.error(e) 
        log.error(f"Please fix me!")
        alerts.generic_error(e)
        
    # Delay by x seconds
    sleep(30*60)