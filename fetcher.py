import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from environment variable
token = os.getenv('GITHUB_TOKEN')


# Replace with the repository details
owner = 'CosmWasm'
repo = 'wasmd'

# GitHub API endpoint to search for issues with security labels
# url = f'https://api.github.com/search/issues?q=repo:{owner}/{repo}+label:security'
url = f'https://api.github.com/repos/CosmWasm/wasmd/security-advisories'

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    advisories = response.json()
    for advisory in advisories:
        ghsa_id = advisory['ghsa_id']
        vulnerabilities = advisory.get('vulnerabilities', [])
        for vuln in vulnerabilities:
            version_range = vuln.get('vulnerable_version_range', 'N/A')
            patched = vuln.get('patched_versions', 'N/A')
            print(f"GHSA ID: {ghsa_id}")
            print(f"  Vulnerable Version Range: {version_range}")
            print(f"  Patched Versions: {patched}")
            print("---")
else:
    print(f"Failed to fetch data: {response.status_code}, {response.text}")