import sys
import logging
import socket

hostname = socket.gethostname()

from includes.config_utils import *

create_data_path((""))
file_handler = logging.FileHandler(filename=os.path.join("logs", "data.log"))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] <%(funcName)s> %(message)s",
    handlers=handlers,
    datefmt="%d-%m-%Y %H:%M:%S",
)
log = logging.getLogger()

# envs = Envs()


VSTATS_API = "https://vstats.one/api/node-stats"

alerts_context = dict(
    envs=envs,
    LOOP_COUNT=0,
    hostname=hostname
)
