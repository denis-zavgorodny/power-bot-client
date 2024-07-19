import os
import requests
from dotenv import dotenv_values
import time

current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)

config = dotenv_values(current_file_dir + "/.env")


def main():
    data = {
        'timestamp': time.time(),
    }

    headers = {
        "API-KEY": config.get("API_KEY")
    }

    response = requests.post(config.get("PING_ENDPOINT"), json=data, headers=headers)

    if response.status_code == 200:
        print('Request was successful')
        print('Response data:', response.json())
    else:
        print('Request failed with status code:', response.status_code)
        print('Response content:', response.text)



if __name__ == '__main__':
    main()

