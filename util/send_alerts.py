import logging as log

from bases.alerts_base import AlertsBase
from includes.config import hostname

class Alerts(AlertsBase):

    def generic_error(self, e: str):
        self.send_alert(
            "Node Stats Script Error -- {self.hostname}",
            e,
            "danger",
            log.error,
            f"Sending ERROR Alert..ERROR  ::  {e}",
        )
        
    def send_data( 
        self,
        node_stats: dict,
        send_shard_0_remote: int,
        send_shard_0_local: int,
        send_shard_main_remote: int,
        send_shard_main_local: int,
        ):
        self.send_alert(
            "Node Stats",
            "Message",
            node_stats,
            send_shard_0_remote,
            send_shard_0_local,
            send_shard_main_remote,
            send_shard_main_local,
            "danger",
            log.info,
            f"Sending Alert",
            )