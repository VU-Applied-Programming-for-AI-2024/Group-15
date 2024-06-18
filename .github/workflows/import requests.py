
import requests
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta, timezone

# Replace these with your own details
GITHUB_TOKEN = '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'
REPO_OWNER = 'VU-Applied-Programming-for-AI-2024'
REPO_NAME = 'Group-15'
DAYS_THRESHOLD = 7  # Number of days to keep artifacts

def get_artifacts():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['artifacts']

def delete_artifact(artifact_id):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/artifacts/{artifact_id}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.status_code == 204

def main():
    artifacts = get_artifacts()
    now = datetime.now(timezone.utc)  # Make now offset-aware with UTC timezone
    threshold_date = now - timedelta(days=DAYS_THRESHOLD)

    for artifact in artifacts:
        created_at = parse_date(artifact['created_at'])

        # Ensure created_at is also offset-aware
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        if created_at < threshold_date:
            print(f"Deleting artifact {artifact['name']} (ID: {artifact['id']}) created at {artifact['created_at']}")
            if delete_artifact(artifact['id']):
                print("Deleted successfully.")
            else:
                print("Failed to delete.")

if __name__ == "__main__":
    main()
