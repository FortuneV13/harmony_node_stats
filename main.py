from time import sleep

from includes.config import *
from util.connect import connect_to_api
from util.tools import *
from util.send_alerts import Alerts

def run():
    while True:
        try:
            log.info(f"Run check")
            
            node_stats = getNodeStats()

            alerts.send_data(node_stats)
            
        except Exception as e:
            alerts.generic_error(e)
            log.error(e)
            log.error(f"Please fix me!")

        # Delay by x seconds
        #sleep(envs.RUN_EVERY_X_MINUTES * 60)
        sleep(60)
        # Hot reload Env
        envs.load_envs()


if __name__ == "__main__":
    alerts = Alerts(VSTATS_API, connect_to_api, **alerts_context)
    run()
