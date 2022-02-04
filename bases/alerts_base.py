import logging as log
from includes.config import *

class AlertsBase:
    def __init__(self, VSTATS_API: str, connect_to_api: object, **kwargs) -> None:
        self.VSTATS_API = VSTATS_API
        self.connect_to_api = connect_to_api
        self.__dict__.update(kwargs)

    def send_to_vstats(self, subject: str, msg: str,node_stats: dict,send_shard_0_remote: int,send_shard_0_local: int,send_shard_main_remote: int,send_shard_main_local: int, load: str, alert_type: str) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN,
            "alert-type": alert_type,
            "subject": subject,
            "message": msg,
            "send_shard-0-remote": send_shard_0_remote,
            "send_shard-0-local": send_shard_0_local,
            "send_shard-main-remote": send_shard_main_remote,
            "send_shard-main-local": send_shard_main_local,
            "node-stats": node_stats,
            "load": load,
            "hostname":self.hostname
        }
        full, _, _ = self.connect_to_api("", self.VSTATS_API, "", j=j)
        log.info(full)

    def send_alert(
        self, subject: str, msg: str,node_stats: dict, send_shard_0_remote: int,send_shard_0_local: int,send_shard_main_remote: int,send_shard_main_local: int, load: str, _type: str,  log_level: log, log_msg: str
    ) -> None:
        log_level(log_msg)
        subject = f"{subject}"
        msg = f"{msg}"
        node_stats = node_stats
        send_shard_0_remote = send_shard_0_remote
        send_shard_0_local = send_shard_0_local
        send_shard_main_remote = send_shard_main_remote
        send_shard_main_local = send_shard_main_local
        load = load
        self.send_to_vstats(subject, msg, node_stats, send_shard_0_remote, send_shard_0_local, send_shard_main_remote, send_shard_main_local,load, _type)


    def generic_error(self) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN
        }
        
        full, _, _ = self.connect_to_api("", self.VSTATS_API, "", j=j)
        log.info(full)
