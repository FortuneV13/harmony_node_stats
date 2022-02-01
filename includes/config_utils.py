import os
from dotenv import dotenv_values, find_dotenv
import logging as log


def create_data_path(pth: str, data_path: str = "logs") -> os.path:
    cwd = os.getcwd()
    p = os.path.join(cwd, data_path, pth)
    if not os.path.exists(p):
        os.mkdir(p)
    return p


class Envs:
    def __init__(self, **kw):
        self.load_envs()

    def load_envs(self):
        config = dotenv_values(find_dotenv())

        for k, v in config.items():
            if not v:
                err = f"No value for key {k} - Please update .env file!"
                log.error(err)
                raise ValueError(err)
            try:
                setattr(self, k, int(v))
            except (SyntaxError, ValueError):
                setattr(
                    self,
                    k,
                    True
                    if v.lower() == "true"
                    else False
                    if v.lower() == "false"
                    else v,
                )
