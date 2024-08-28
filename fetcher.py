import requests
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from environment variable
token = os.getenv('GITHUB_TOKEN')


# Replace with the repository details
parser = argparse.ArgumentParser(description='Fetch security advisories for a GitHub repository.')
parser.add_argument('owner', help='The owner of the repository')
parser.add_argument('repo', help='The name of the repository')
args = parser.parse_args()

owner = args.owner
repo = args.repo

# GitHub API endpoint to search for issues with security labels
url = f'https://api.github.com/repos/{owner}/{repo}/security-advisories'

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    advisories = response.json()
    for advisory in advisories:
        ghsa_id = advisory['ghsa_id']
        title = advisory['summary']
        vulnerabilities = advisory.get('vulnerabilities', [])
        print(f"GHSA ID: {ghsa_id}")
        print(f"Title: {title}")

        vulnerabilities = advisory.get('vulnerabilities', [])
        for vuln in vulnerabilities:
            version_range = vuln.get('vulnerable_version_range', 'N/A')
            patched = vuln.get('patched_versions', 'N/A')
            print(f"  Vulnerable Version Range: {version_range}")
            print(f"  Patched Versions: {patched}")
            print("---")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")