import requests
from operator import itemgetter

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
token = os.getnenv("GITHUB_TOKEN")