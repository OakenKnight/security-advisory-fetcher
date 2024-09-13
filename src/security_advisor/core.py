import requests
from typing import List, Dict
from .utils import load_github_token
import csv
from dataclasses import dataclass

@dataclass
class Repository:
    owner: str
    name: str

def read_partners_csv(file_path: str) -> list[Repository]:
    repositories = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) == 2:
                owner, repo = row
                repositories.append(Repository(owner=owner.strip(), name=repo.strip()))
    return repositories

def fetch_github_advisories(owner: str, repo: str) -> List[Dict]:
    token = load_github_token()
    url = f'https://api.github.com/repos/{owner}/{repo}/security-advisories'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [extract_advisory_data(advisory, owner, repo) for advisory in response.json()]
    else:
        raise Exception(f"Requested url: {url}; Failed to fetch data: {response.status_code}, {response.text}")

def extract_advisory_data(advisory: Dict, owner: str, repo: str) -> Dict:
    ghsa_id = advisory['ghsa_id']
    return {
        "GHSA ID": ghsa_id,
        "Repository": f"https://github.com/{owner}/{repo}",
        "Title": advisory['summary'],
        "Severity": advisory['severity'],
        "Advisory URL": f"https://github.com/advisories/{ghsa_id}",
        "Vulnerabilities": [
            {
                "Vulnerable Version Range": vuln.get('vulnerable_version_range', 'N/A'),
                "Patched Versions": vuln.get('patched_versions', 'N/A')
            }
            for vuln in advisory.get('vulnerabilities', [])
        ]
    }
