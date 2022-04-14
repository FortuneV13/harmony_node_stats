import os
import simplejson
from time import sleep
from includes.config import *
from subprocess import PIPE, Popen

#robo
# def get_json_for_command(process_args, retries=3, retry_wait=0.1):
#     original_process_args = process_args[:]
#     if config.USE_REMOTE_NODE:
#         process_args.extend(["--node", config.NODE_API_URL])
#     process = Popen(process_args, stdout=PIPE)
#     (output, err) = process.communicate()
#     try:
#         return simplejson.loads(output)
#     except simplejson.JSONDecodeError:
#         sleep(retry_wait)
#         print(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
#               f"retrying after {retry_wait}s")
#         if retries > 0:
#             return get_json_for_command(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
#     return None


def get_json_for_command_nodeStats(process_args, retries=3, retry_wait=0.1):
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
    return None
    
def get_json_for_command_sync(process_args, retries=3, retry_wait=0.1):
    original_process_args = process_args[:]
    process = Popen(process_args, stdout=PIPE)
    (output, err) = process.communicate()
    try:
        return simplejson.loads(output)
    except simplejson.JSONDecodeError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
              f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_sync(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None

def get_json_for_command_sync_remote(process_args, url, retries=3, retry_wait=0.1):
    original_process_args = process_args[:]
    process_args.extend(["--node", url])
    process = Popen(process_args, stdout=PIPE)
    (output, err) = process.communicate()
    try:
        return simplejson.loads(output)
    except simplejson.JSONDecodeError:
        sleep(retry_wait)
        log.error(f"Got an error in get_json_for_command({' '.join(process_args)}), output={output}, err={err}, "
              f"retrying after {retry_wait}s")
        if retries > 0:
            return get_json_for_command_sync_remote(original_process_args, url, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None
 
def getNodeStats():
    return get_json_for_command_nodeStats([envs.HARMONY_FOLDER+"/hmy", "utility", "metadata"])
    
def getSyncLocal():
    return get_json_for_command_sync([envs.HARMONY_FOLDER+"/hmy", "blockchain", "latest-headers"])
 
def getSyncRemote(url):
    return get_json_for_command_sync_remote([envs.HARMONY_FOLDER+"/hmy", "blockchain", "latest-headers"],url)    
        

    
    
    
    

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

