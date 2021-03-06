import logging as log
from includes.config import *

class Alerts:
    def __init__(self, VSTATS_API: str, connect_to_api: object, **kwargs) -> None:
        self.VSTATS_API = VSTATS_API
        self.connect_to_api = connect_to_api
        self.__dict__.update(kwargs)

    def send_to_vstats(self,node_stats: dict,send_shard_0_remote: int,send_shard_0_local: int,send_shard_main_remote: int,send_shard_main_local: int, load: str,space:str,count:int) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN,
            "validator_address": self.envs.VALIDATOR_ADDRESS,
            "double_sign_check_enabled": self.envs.DOUBLE_SIGN_CHECK_ENABLED,
            "sync_check_enabled": self.envs.SYNC_CHECK_ENABLED,
            "space_check_enabled": self.envs.SPACE_CHECK_ENABLED,
            "send_shard-0-remote": send_shard_0_remote,
            "send_shard-0-local": send_shard_0_local,
            "send_shard-main-remote": send_shard_main_remote,
            "send_shard-main-local": send_shard_main_local,
            "node-stats": node_stats,
            "load": load,
            "space":space,
            "hostname":self.hostname,
            "count":count
        }
        full, _, _ = self.connect_to_api("", self.VSTATS_API, "", j=j)
        log.info(full)


    def generic_error(self,e) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN,
            "error": 'true',
            "hostname":self.hostname
        }
        
        full, _, _ = self.connect_to_api("", self.VSTATS_API, "", j=j)
        log.info(full)
