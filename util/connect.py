import requests
import json

from util.tools import flatten
import logging as log


def connect_to_api(
    token: str,
    api: str,
    endpoint: str,
    call: requests = requests.get,
    j: dict = {},
    key: str = "",
    rtn_data: tuple = (),
    resize_msg="",
) -> dict:

    rtn = {}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        r = call(api + endpoint, json=j, headers=headers)
        if r.status_code == 401:
            auth = "Authorisation failed [401] Please check your Token and regenerate a new one if required"
            log.error(auth)
            return auth, r.text, resize_msg
        data = r.json()
    except json.decoder.JSONDecodeError as e:
        data = r.text
        log.error(f"Problem with API {e}")

    try:
        if data.get("errors"):
            return data, data, resize_msg
        if data.get("id"):
            if data["id"] == "unprocessable_entity":
                return data, data, resize_msg
    except AttributeError as e:
        log.error(e)
        return data, data, e

    rtn = data

    if rtn_data:
        try:
            rtn = {k: v for k, v in data[key].items() if k in rtn_data}
        except (KeyError, AttributeError) as e:
            try:
                rtn = {k: v for k, v in data.items() if k in rtn_data}
            except AttributeError:
                pass

    return rtn, flatten(rtn), resize_msg
