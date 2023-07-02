import logging

import requests
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_random_exponential
from tenacity.before_sleep import before_sleep_log

from config.config import _get_nimble_credential_string, config
from src.utils import _get_domain


@retry(
    wait=wait_random_exponential(min=30, max=60),
    stop=stop_after_attempt(3),
    before_sleep=before_sleep_log(logger, logging.DEBUG),
)
def hit_nimble_api(url):
    nimble_api_url = "https://api.webit.live/api/v1/realtime/web"
    headers = {
        "Authorization": f"Basic {_get_nimble_credential_string()}",
        "Content-Type": "application/json",
        "authority": _get_domain(url),
        "user-agent": config["nimble"]["user_agent"],
    }
    data = {"url": url}
    render = config["nimble"]["render"]
    if render:
        render_config = {
            "render": render,
            "render_type": config["nimble"]["render_type"],
            "timeout": config["nimble"]["timeout"],
        }
        data.update(render_config)

    response = requests.post(nimble_api_url, headers=headers, json=data)
    if not response.ok:
        logger.error(f"Error while making Nimble API request: {response.json()}")
    response.raise_for_status()
    return response.json()["html_content"]
