import os
import simplejson
from time import sleep
from includes.config import *
from subprocess import PIPE, Popen

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
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
              f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_sync_remote(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    except KeyError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
            f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_nodeStats(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None
 
def getNodeStats(shardValue:dict):
    if shardValue['http_port']: 
        return get_json_for_command_nodeStats([shardValue["harmony_folder"]+"/hmy", "utility", "metadata","--node","http://localhost:"+shardValue['http_port']])
    else:
        return get_json_for_command_nodeStats([shardValue["harmony_folder"]+"/hmy", "utility", "metadata"])
    
def getSyncLocal(shardValue:dict):
    if shardValue['http_port']: 
        return get_json_for_command_sync([shardValue["harmony_folder"]+"/hmy", "blockchain", "latest-headers","--node","http://localhost:"+shardValue['http_port']])
    else:
        return get_json_for_command_sync([shardValue["harmony_folder"]+"/hmy", "blockchain", "latest-headers"])
 
def getSyncRemote(shardValue:dict,url):
    return get_json_for_command_sync_remote([shardValue["harmony_folder"]+"/hmy", "blockchain", "latest-headers","--node",url])    
        

    
    
    
    

def flatten(d: dict) -> None:
    """Flatten a nested dictionary.

    Args:
        d (dict): nested dictionary to flatten

    Returns:
        dict: flattened dictionary.
    """
    out = {}
    if d:
        if isinstance(d, str):
            import ast

            try:
                d = ast.literal_eval(d)
            except (ValueError, SyntaxError):
                pass
        try:
            for key, val in d.items():
                if isinstance(val, dict):
                    val = [val]
                if isinstance(val, list):
                    for subdict in val:
                        deeper = flatten(subdict).items()
                        out.update(
                            {
                                key2: val2
                                for key2, val2 in deeper
                                if key2 not in out.keys()
                            }
                        )
                else:
                    out[key] = val
        except AttributeError as e:
            pass
    return out

