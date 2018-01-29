import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))
ACCSES_TOKEN = os.environ.get("API_TOKEN")

if __name__ == '__main__':
    print(ACCSES_TOKEN)
