import csv
import json
import requests
import sys
from typing import List, Dict, Optional

def fetch_github_data(owner: str, repo: str) -> List[Dict]:
    url = f"https://api.github.com/repos/{owner}/{repo}/security-advisories"
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        advisories = response.json()
        return [extract_advisory_data(advisory) for advisory in advisories]
    else:
        return [{"error": f"Failed to fetch data for {owner}/{repo}"}]

def extract_advisory_data(advisory: Dict) -> Dict:
    ghsa_id = advisory['ghsa_id']
    return {
        "GHSA ID": ghsa_id,
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

def process_csv_and_save_json(input_file: str, output_file: str):
    results = []
    
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                owner, repo = row
                data = fetch_github_data(owner, repo)
                results.extend(data)
    
    with open(output_file, 'w') as jsonfile:
        json.dump(results, jsonfile, indent=2)

def process_single_repo(owner: str, repo: str):
    data = fetch_github_data(owner, repo)
    print(json.dumps(data, indent=2))

def main(args: List[str]):
    if len(args) == 2:
        owner, repo = args
        process_single_repo(owner, repo)
    elif len(args) == 0:
        process_csv_and_save_json("data/sources.csv", "data/out.json")
        print("Data saved to out.json")
    else:
        print("Usage: python fetch_github_data.py [owner repo]")
        print("If no arguments are provided, data will be fetched from sources.csv")

if __name__ == "__main__":
    main(sys.argv[1:])