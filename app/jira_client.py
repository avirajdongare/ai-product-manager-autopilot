import os
from dotenv import load_dotenv
from jira import JIRA

load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

def get_jira_client():
    options = {"server": JIRA_SERVER}
    return JIRA(
        options=options,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

def create_jira_issue(summary, description):
    jira = get_jira_client()
    try:
        issue = jira.create_issue(
            project=JIRA_PROJECT_KEY,
            summary=summary,
            description=description,
            issuetype={"name": "Task"}
        )
        return {
            "key": issue.key,
            "link": f"{JIRA_SERVER}/browse/{issue.key}"
        }
    except Exception as e:
        print(f"Jira ticket creation failed: {e}")
        return None
