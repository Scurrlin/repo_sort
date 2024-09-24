# Repo Sort

![Repo Sort Banner](./assets/RS_meme1.jpg)

Okay maybe the world wouldn't look EXACTLY like that if you could sort your repositories, but you get the idea. While I love GitHub and think it’s a wonderful platform, I'm surprised that there’s no option to set default sorting preferences.

Even though this is a minor problem, I've created a lightweight script that uses your profile `README.md` to display your repos using alternative sorting methods.

## Getting Started

For this script to run properly, you'll need the `requests` and `python-dotenv` modules. You can install them using the following command:

```bash
pip3 install requests python-dotenv
```

For the script itself, you can copy the code directly from the repo_sort.py file above or the snippet below. It is also worth noting that this script is written to display repos by date created starting with the most recent.

If you want to sort by another method like number of commits, you'll need to update that part of the code accordingly.

<details>
<summary><code>repo_sort.py</code></summary>

```python
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
    "HTML": "🔴",
    "JavaScript": "🟡",
    "Python": "🔵",
    "TypeScript": "🔵",
    "PHP": "🟣",
    "C++": "🔴"
}

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
<a name="top"></a>

# Hi, I'm <Your Name> 👋

<table>
<tr>
<td>
Introduce yourself here!
</tr>
</table>

### Skills/Tools:

![My Skills](https://skillicons.dev/icons?i=js,react,express,mongodb,nodejs,nextjs,threejs,tailwind,python,django,flask,postgres,postman,vercel,git)

### [Skip to Contributions](#contributions)

### Repositories sorted by date created:
"""

repos_per_page = 30
total_pages = (len(sorted_repos) + repos_per_page - 1) // repos_per_page

for page_num in range(total_pages):
    readme_content += f"## Page {page_num + 1}\n\n"

    start_index = page_num * repos_per_page
    end_index = start_index + repos_per_page
    page_repos = sorted_repos[start_index:end_index]

    for index, repo in enumerate(page_repos):
        formatted_date = repo['created_at'][:10]

        # Reformat the date from YYYY-MM-DD to MM-DD-YYYY
        year, month, day = formatted_date.split('-')
        formatted_date = f"{month}-{day}-{year}"

        # Get the primary language and its color
        language = repo['language']
        language_color = language_colors.get(language, "")

        # Handle forked repos
        if repo['fork']:
            # Check if parent info is available
            if 'parent' not in repo:
                # Make additional request to get the full repo details
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

        # Add the repository to the README content
        readme_content += f"### [{repo['name']}]({repo['html_url']})\n"
        readme_content += f"{language_color} {language} • Created on {formatted_date}  \n{fork_info}\n\n"

        # Omit separator if it's the last repository on the page
        if index < len(page_repos) - 1:
            readme_content += "---\n\n"

# Add an anchor tag at the end for "Skip to Contributions"
readme_content += "\n<a name='contributions'></a>\n"

# Add the "Back to Top" link at the bottom
readme_content += """
### [Back to Top](#top)
"""

# Write the generated content to the README.md file
with open("README.md", "w") as readme_file:
    readme_file.write(readme_content)

print("README.md updated with static content and paginated repositories.")

# Stage the changes, commit, and push to GitHub using subprocess
subprocess.run(["git", "add", "README.md"], check=True)
subprocess.run(["git", "commit", "-m", "updated sorted repos"], check=True)
subprocess.run(["git", "push"], check=True)

print("Changes committed and pushed to GitHub.")
```

</details>

## Setting Up Environment Variables

Once you've personalized the script, you'll need to set up your environment variables. Create a new file named `.env` in the root of your project and add the following two variables. Don't forget to include them in your `.gitignore`!

```env
GITHUB_USERNAME=
GITHUB_TOKEN=
```

To get your GitHub Personal Access Token, follow the steps below:

<details>
<summary>Generate a GitHub Personal Access Token</summary>

1. Log in to your **GitHub** account.
2. Click on your **profile picture**, then select **Settings** from the dropdown menu.
3. On the left-hand sidebar, scroll down and click on **Developer settings**.
4. Under **Developer settings**, click on **Personal access tokens**.
5. Select **Tokens (classic)**.
6. Click **Generate new token**.
7. Set the **token name**, select the `repo` and `read:user` **permissions**, and finally click **Generate token**.
8. Copy the token immediately as you won’t be able to view it again later.

</details>

## Running the Script

After you've updated the code to your liking and added in your environment variables, use the following command to run the script:

```bash
python3 repo_sort.py
```