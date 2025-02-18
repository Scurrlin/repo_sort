import requests
from operator import itemgetter
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

language_colors = {
    "HTML": "🟠",
    "CSS": "🟣",
    "JavaScript": "🟡",
    "TypeScript": "🔵",
    "Python": "🔵",
    "PHP": "🟣",
    "C++": "🔴",
    "C#": "🟢",
    "C": "⚪️"
}

# Fetch all repos
while True:
    response = requests.get(
        f"{url}?page={page}&per_page={per_page}",
        auth=(username, token)
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

# Sort repos by date created
sorted_repos = sorted(all_repos, key=itemgetter('created_at'), reverse=True)

# Build main README content
readme_content = """
<a name="top"></a>

# Hi, I'm Sean 👋

<table>
<tr>
<td>
I have a demonstrated proficiency in software development, with a proven track record of delivering high-quality solutions from ideation to deployment...
</td>
</tr>
</table>

### Skills/Tools:

![My Skills](https://skillicons.dev/icons?i=js,react,express,mongodb,nodejs,nextjs,threejs,tailwind,python,django,flask,postgres,postman,vercel,git)

### [Skip to Contributions](#contributions)

### Repositories sorted by date created:
"""

# Calculate pagination details
repos_per_page = 30
total_pages = (len(sorted_repos) + repos_per_page - 1) // repos_per_page

# Loop through each page of repositories
for page_num in range(total_pages):
    current_page = page_num + 1

    # Create anchor
    readme_content += f'<a name="page{current_page}"></a>\n'

    # Build the page headline
    page_links = []
    for i in range(1, total_pages + 1):
        if i == current_page:
            page_links.append(f"{i}")
        else:
            page_links.append(f"[{i}](#page{i})")

    heading_line = " • ".join(page_links)
    readme_content += f"## Page {heading_line}\n\n"

    start_index = page_num * repos_per_page
    end_index = start_index + repos_per_page
    page_repos = sorted_repos[start_index:end_index]

    for index, repo in enumerate(page_repos):
        formatted_date = repo['created_at'][:10]
        year, month, day = formatted_date.split('-')
        formatted_date = f"{month}-{day}-{year}"

        # Always fetch from the /languages endpoint
        languages_url = repo['languages_url']
        lang_response = requests.get(languages_url, auth=(username, token))
        language = repo['language']
        
        if lang_response.status_code == 200:
            lang_data = lang_response.json()
            if lang_data:

                # Find main language
                main_lang = max(lang_data, key=lang_data.get)
                
                # Log language change if needed
                if main_lang != language:
                    print(f"Repo '{repo['name']}' language changed from {language} to {main_lang}")
                language = main_lang
        language_color = language_colors.get(language, "")

        # Handle fork info
        if repo['fork']:
            if 'parent' not in repo:
                repo_details_url = repo['url']
                repo_details_response = requests.get(repo_details_url, auth=(username, token))
                if repo_details_response.status_code == 200:
                    repo_details = repo_details_response.json()
                    if 'parent' in repo_details:
                        parent = repo_details['parent']['full_name']
                        fork_info = f"🍴 Forked from [{parent}](https://github.com/{parent})"
                    else:
                        fork_info = "🍴 Forked from unknown"
                else:
                    print(f"Failed to fetch parent details: {repo_details_response.status_code}")
                    fork_info = "🍴 Forked from unknown"
            else:
                parent = repo['parent']['full_name']
                fork_info = f"🍴 Forked from [{parent}](https://github.com/{parent})"
        else:
            fork_info = ""

        readme_content += f"### [{repo['name']}]({repo['html_url']})\n"
        readme_content += f"{language_color} {language if language else 'None'} • Created on {formatted_date}  \n{fork_info}\n\n"

        if index < len(page_repos) - 1:
            readme_content += "---\n\n"

# Final anchors and closing
readme_content += "\n<a name='contributions'></a>\n"
readme_content += """
### [Back to Top](#top)
"""

# Write the README file
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

# Git commit & push
subprocess.run(["git", "add", "README.md"], check=True)
subprocess.run(["git", "commit", "-m", "Update README with new pagination format"], check=True)
subprocess.run(["git", "push"], check=True)

print("Changes committed and pushed to GitHub.")