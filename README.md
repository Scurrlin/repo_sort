# Repo Sort

![Repo Sort Banner](./assets/RS_meme1.jpg)

Skip to Snippets

Okay maybe the world wouldn't look EXACTLY like that if you could sort your repositories, but you get the idea. Though I do love GitHub and think it is a wonderful platform, I find the inability to select a default sort parameter for your repos surprising. Additionally, there are only three sorting methods to choose from:

1.) Last updated (locked default setting)
2.) Name
3.) Stars

While this is certainly a minor problem, I've created a lightweight script that uses your profile readme to display your repositories using altrenative sorting options.

**But why, Sean?**

I'm glad you asked! I recently retired some older projects of mine and part of the process involved removing the live link from their respective READMEs. Upon doing so, because "Last updated" is the default sorting option for your repositories, the older repos jumped up to the top of the list.

Now in the event that someone wants to check through my work on GitHub, the first project they will see is one of my earliest, least polished efforts. Again, this isn't the end of the world, but it's also not ideal.

**Getting Started**

You can copy the code directly from the repo_sort.py file above or the snippet below:

<details>
    <summary>repo_sort.py</summary>

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
        "PHP": "🟣"
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

    # Hi, I'm <Name> 👋

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
    
</details>```

**Set Up Environment Variables**

Create a new file named `.env` in the root of your project and add the following content:

```env
GITHUB_USERNAME=
GITHUB_TOKEN=
```