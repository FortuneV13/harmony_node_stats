import logging as log
from includes.setup import *
from config import *
import socket
import json
import requests

class Alerts:
    def send_to_vstats(self,shardKey:str,node_stats: dict,send_shard_0_remote: int,send_shard_0_local: int,send_shard_main_remote: int,send_shard_main_local: int, load: str,space:str,count:int) -> None:
        params = {
            "array_key": shardKey,
            "send_shard-0-remote": send_shard_0_remote,
            "send_shard-0-local": send_shard_0_local,
            "send_shard-main-remote": send_shard_main_remote,
            "send_shard-main-local": send_shard_main_local,
            "node-stats": node_stats,
            "load": load,
            "space":space,
            "hostname":socket.gethostname(),
            "count":count
        }
        self.connect_to_api(params)
        # log.info(full)
    
    def connect_to_api(self, params: dict) -> None:
        headers = {"Authorization": f"Bearer {VSTATS_TOKEN}", "Content-Type": "application/json"}
        try:
            response = requests.post(VSTATS_API, headers=headers, json=params, verify=True)
            if response.status_code == 401:
                auth = "Authorisation failed [401] Please check your Token and regenerate a new one if required"
                log.error(auth)
            elif response.status_code == 200:
                print(response.status_code)
                print(response.text)
            else:
                print(response)
                print("Unknown Error")
        except json.decoder.JSONDecodeError as e:
            log.error(f"Problem with API {e}")
    
    def generic_error(self,e) -> None:
        j = {
            "error": 'true',
            "hostname":socket.gethostname()
        }
        self.connect_to_api(j=j)
    
alerts = Alerts()