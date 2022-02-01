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
        node_stats: str,
        ):
        self.send_alert(
            "Node Stats",
            "Message",
            node_stats,
            "danger",
            log.info,
            f"Sending Alert",
            )
