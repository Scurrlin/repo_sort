import requests
from operator import itemgetter
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")

url = f"https://api.github.com/users/{username}/repos"

all_repos = []
page = 1
per_page = 30

est = pytz.timezone('US/Eastern')

while True:
    response = requests.get(
        f"{url}?page={page}&per_page={per_page}", auth=(username, token)
    )

    if response.status_code == 200:
        repos = response.json()
        if repos:
            all_repos.extend(repos)
            page += 1
        else:
            break

    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        break

sorted_repos = sorted(all_repos, key=itemgetter('created_at'), reverse=True)

# Static README content you want to keep above your repo list

readme_content = """
# Hi, I'm Sean 👋

<table>
<tr>
<td>
I have a demonstrated proficiency in software development, with a proven track record of delivering high-quality solutions from ideation to deployment. My expertise includes developing and optimizing web applications, enhancing data pipelines, and implementing analytics to generate actionable insights. I possess a deep understanding of full-stack development, particularly in Python, JavaScript, React.js, and database management. My polished communication skills enable me to effectively articulate complex technical strategies.
</td>
</tr>
</table>

## I've worked with:

### Skills/Tools:

![My Skills](https://skillicons.dev/icons?i=js,react,express,mongodb,nodejs,nextjs,threejs,tailwind,python,django,flask,postgres,postman,vercel,git)


| Skills        |               |
| ------------- | ------------- |
| JavaScript    | Python        |
| React         | Django        |
| Express       | Flask         |
| NodeJS        | PostgreSQL    |
| NextJS        | Render        |
| ThreeJS       | Hostinger     |
| MongoDB       | Vercel        |
| Tailwind CSS  | Postman API   |
| Payload CMS   | REST Framework|
| Appwrite BaaS | Git           |

## Repositories sorted by date created

"""

repos_per_page = 30
total_pages = (len(sorted_repos) + repos_per_page - 1) // repos_per_page

for page_num in range(total_pages):
    readme_content += f"## Page {page_num + 1}\n\n"
    
    # Get the start and end index for this page
    start_index = page_num * repos_per_page
    end_index = start_index + repos_per_page
    page_repos = sorted_repos[start_index:end_index]
    
    for repo in page_repos:
        # Parse the UTC creation date
        utc_time = datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        est_time = utc_time.replace(tzinfo=pytz.utc).astimezone(est)

        # Format the date and time in EST
        formatted_date = est_time.strftime("%m-%d-%Y")
        formatted_time = est_time.strftime("%I:%M %p")

        # Get the last updated date in EST
        last_updated_utc = datetime.strptime(repo['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        last_updated_est = last_updated_utc.replace(tzinfo=pytz.utc).astimezone(est)
        last_updated_formatted = last_updated_est.strftime("%m-%d-%Y %I:%M %p")

        # Get the repo description (if available)
        description = repo['description'] if repo['description'] else "No description"

        # Get the primary language (if available)
        language = repo['language'] if repo['language'] else "Unknown"

        # Add the repository to the README content with formatting
        readme_content += f"### [{repo['name']}]({repo['html_url']})\n"
        readme_content += f"- **Description**: {description}\n"
        readme_content += f"- **Primary language**: {language}\n"
        readme_content += f"- **Created on**: {formatted_date} at {formatted_time} EST\n"
        readme_content += f"- **Last updated**: {last_updated_formatted} EST\n\n"

# Write to the README.md file in the repository
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

print("README.md updated with personal content and paginated repositories.")

# Stage the changes, commit, and push to GitHub using subprocess
subprocess.run(["git", "add", "README.md"], check=True)
subprocess.run(["git", "commit", "-m", "Updated README with sorted repositories"], check=True)
subprocess.run(["git", "push"], check=True)

print("Changes committed and pushed to GitHub.")