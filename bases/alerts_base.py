import logging as log
from includes.config import *
class AlertsBase:
    def __init__(self, VSTATS_API: str, connect_to_api: object, **kwargs) -> None:
        self.VSTATS_API = VSTATS_API
        self.connect_to_api = connect_to_api
        self.__dict__.update(kwargs)

    def send_to_vstats(self, subject: str, msg: str,node_stats: dict, alert_type: str) -> None:
        j = {
            "api_token": self.envs.VSTATS_TOKEN,
            "alert-type": alert_type,
            "subject": subject,
            "message": msg,
            "node-stats": node_stats,
            "validator-address": envs.VALIDATOR_ADDRESS,
            "hostname":self.hostname
        }
        full, _, _ = self.connect_to_api("", self.VSTATS_API, "", j=j)
        log.info(full)

    def send_alert(
        self, subject: str, msg: str,node_stats: dict, _type: str, log_level: log, log_msg: str
    ) -> None:
        log_level(log_msg)
        subject = f"{subject}"
        msg = f"{msg}"
        node_stats = node_stats
        self.send_to_vstats(subject, msg,node_stats, _type)
