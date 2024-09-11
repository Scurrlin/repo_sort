import requests
from operator import itemgetter

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")

url = f"https://api.github.com/users/{username}/repos"

response = requests.get(url, auth=(username, token))

if response.status_code == 200:
    repos = response.json()

    sorted_repos = sorted(repos, key=itemgetter('created_at'), reverse=True)

    print("Repositories sorted by date created:")
    for repo in sorted_repos:
        print(f"{repo['name']} - Created on {repo['created_at']}")
else:
    print(f"Failed to fetch repositories: {response.status_code}")