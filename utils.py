import os
import os.path
import subprocess
import simplejson
from time import sleep
from subprocess import PIPE, Popen
from logging_util import setup_logging
import requests
import subprocess
import sys
from config import VSTATS_API, VSTATS_TOKEN

# Setup log
log = setup_logging()


def check_service_status(service_name):
    try:
        # Check if service is enabled
        output_enabled = subprocess.check_output(['systemctl', 'is-enabled', service_name], text=True).strip()
        is_enabled = True if output_enabled == 'enabled' else False
    except subprocess.CalledProcessError:
        # Assume False if the service does not exist or other errors occur for 'is-enabled'
        is_enabled = False

    try:
        # Check if service is active
        output_active = subprocess.check_output(['systemctl', 'is-active', service_name], text=True).strip()
        is_active = True if output_active == 'active' else False
    except subprocess.CalledProcessError:
        # Assume False if the service does not exist or other errors occur for 'is-active'
        is_active = False

    return is_enabled, is_active


def get_json_for_command_nodeStats(process_args, retries=10, retry_wait=1.0):
    original_process_args = process_args[:]
    process = Popen(process_args, stdout=PIPE)
    (output, err) = process.communicate()
    try:
        routput = simplejson.loads(output)
        return routput['result']
    except simplejson.JSONDecodeError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
            f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_nodeStats(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    except KeyError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
            f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_nodeStats(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None
    
def get_json_for_command_sync(process_args, retries=10, retry_wait=1.0):
    original_process_args = process_args[:]
    process = Popen(process_args, stdout=PIPE)
    (output, err) = process.communicate()
    try:
        routput = simplejson.loads(output)
        return routput['result']
    except simplejson.JSONDecodeError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
              f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_sync(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    except KeyError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
            f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_nodeStats(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None

def get_json_for_command_sync_remote(process_args, retries=10, retry_wait=1.0):
    original_process_args = process_args[:]
    # process_args.extend(["--node", url])
    process = Popen(process_args, stdout=PIPE)
    (output, err) = process.communicate()
    try:
        routput = simplejson.loads(output)
        return routput['result']
    except simplejson.JSONDecodeError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_sync_remote(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    except KeyError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
            f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_nodeStats(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None

def getNodeStats(node:dict):
    if node['http_port']: 
        return get_json_for_command_nodeStats([node["harmony_folder"]+"/hmy", "utility", "metadata","--node","http://localhost:"+f'{node["http_port"]}'])
    else:
        return get_json_for_command_nodeStats([node["harmony_folder"]+"/hmy", "utility", "metadata"])
    
def getSyncLocal(node: dict, shardID: int):
    if node['http_port']: 
        var = get_json_for_command_sync([node["harmony_folder"]+"/hmy", "blockchain", "latest-headers", "--node", "http://localhost:" + f'{node["http_port"]}'])
    else:
        var = get_json_for_command_sync([node["harmony_folder"]+"/hmy", "blockchain", "latest-headers"])

    # Adjusting for hexadecimal conversion
    block_number_hex = var.get('beacon-chain-header' if shardID == 0 else 'shard-chain-header', {}).get('number', "0x0")
    return int(block_number_hex, 16)


def getSyncRemote(node: dict, url: str):
    var = get_json_for_command_sync_remote([node["harmony_folder"]+"/hmy", "blockchain", "latest-headers", "--node", url])
    
    # Adjusting for hexadecimal conversion
    block_number_hex = var['shard-chain-header']['number']
    return int(block_number_hex, 16)


def get_available_space():
    try:
        # Assuming you want to check the available space on the filesystem of the current directory
        space_output = subprocess.check_output(['df', '-BG', '--output=avail', '.'], stderr=subprocess.STDOUT).splitlines()[-1]
        return space_output.decode().strip()
    except subprocess.CalledProcessError as e:
        log.error(f"Problem getting space: {e.output.decode()}")
        return None
    except Exception as e:
        log.error(f"Unexpected error getting space: {e}")
        return None

def post_to_vstats(data):
    try:
        response = requests.post(VSTATS_API, headers={"Authorization": f"Bearer {VSTATS_TOKEN}", "Content-Type": "application/json"}, json=data, verify=True)
        log.info('Data successfully sent to vStats')
        log.info(response)
    except Exception as e:
        log.error(f"Connection Error to vStats servers: {e}")