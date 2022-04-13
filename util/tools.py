import os
import simplejson
from time import sleep
from includes.config import *
from subprocess import PIPE, Popen



def get_json_for_command(process_args, retries=3, retry_wait=0.1):
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
            return get_json_for_command(original_process_args, retries=retries - 1, retry_wait=retry_wait * 1.25)
    return None
 
def getNodeStats():
    return get_json_for_command([envs.HARMONY_FOLDER+"/hmy", "utility", "metadata"])
    
        
# def getNodeStats() -> dict:
#     mode = ""
#     for x in range(5):
#         try:
#             ourVersion = subprocess.getoutput(f"{envs.HARMONY_FOLDER}/hmy utility metadata")
#             str1 = json.loads(ourVersion)
#             if "result" in str1:
#                 if "consensus" in str1["result"]:
#                     mode = str1["result"]
#                     return mode
#                     break
#                 else:
#                     time.sleep(3) 
#             else:
#                 time.sleep(3)  
#         except:
#             mode = "error"
#             log.error("Node stats - Signing mode could not be found")
#     return mode 
    
    
    


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

