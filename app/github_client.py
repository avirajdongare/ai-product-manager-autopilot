import os
from github import Github
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def create_github_issue(title, body):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        issue = repo.create_issue(title=title, body=body)
        return {
            "number": issue.number,
            "url": issue.html_url
        }
    except Exception as e:
        print(f"GitHub Issue creation failed: {e}")
        return None
