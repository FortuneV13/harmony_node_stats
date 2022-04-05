import subprocess
import os
import json
import time
from includes.config import *


def getNodeStats() -> str:
    mode = ""
    for x in range(5):
        print(x)
        try:
            ourVersion = subprocess.getoutput(f"{envs.HARMONY_FOLDER}/hmy utility metadata")
            str1 = json.loads(ourVersion)
            if "result" in str1:
                mode = (str1["result"])
                return mode
                break
            else:
                log.error("Node stats - Signing mode could not be found")
                time.sleep(3)  
        except:
            mode = "error"
            log.error("Node stats - Signing mode could not be found")
    return mode 
    
    
    


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

