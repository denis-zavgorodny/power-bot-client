import os
import requests
from requests.adapters import HTTPAdapter
import logging

from dotenv import dotenv_values
import time
from urllib3.util.retry import Retry

logger = logging.getLogger("power-bot-sensor")
logging.basicConfig(
    filename="power-bot-sensor.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)

config = dotenv_values(current_file_dir + "/.env")


def main():
    try:

        data = {
            'timestamp': time.time(),
        }

        headers = {
            "API-KEY": config.get("API_KEY")
        }

        session = requests_session_with_retries(retries=5, backoff_factor=0.5)

        response = session.post(config.get("PING_ENDPOINT"), json=data, headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            print('Request was successful')
            print('Response data:', response.json())
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
            logger.error(f"Response content: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Status POST request failed: {e}")


def requests_session_with_retries(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


if __name__ == '__main__':
    main()

