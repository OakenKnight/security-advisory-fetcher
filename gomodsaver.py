import csv
import os
import requests
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from tqdm import tqdm 
# Load environment variables from .env file
load_dotenv()
# Add your GitHub personal access token here
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
def get_go_mod_files(owner: str, repo: str, path: str = '') -> Tuple[List[Dict], int]:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching contents for {owner}/{repo}/{path}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return [], 0

    contents = response.json()
    go_mod_files = []
    main_dir_count = 0

    if isinstance(contents, dict) and contents.get('type') == 'file' and contents.get('name') == 'go.mod':
        # This is a direct go.mod file
        file_content = get_file_content(contents['download_url'])
        go_mod_files.append({
            'repo': f"{owner}/{repo}",
            'path': contents['path'],
            'content': file_content
        })
        main_dir_count = 1 if path == '' else 0
    elif isinstance(contents, list):
        for item in contents:
            if item['type'] == 'file' and item['name'] == 'go.mod':
                file_content = get_file_content(item['download_url'])
                go_mod_files.append({
                    'repo': f"{owner}/{repo}",
                    'path': item['path'],
                    'content': file_content
                })
                if path == '':  # This is the main directory
                    main_dir_count = 1
            elif item['type'] == 'dir':
                sub_files, sub_count = get_go_mod_files(owner, repo, item['path'])
                go_mod_files.extend(sub_files)

    return go_mod_files, main_dir_count

def get_file_content(url: str) -> str:
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching file content from {url}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return "Error fetching file content"

def save_go_mod_file(base_dir: str, repo: str, path: str, content: str):
    full_path = os.path.join(base_dir, repo, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as file:
        file.write(content)

def process_repos(input_file: str, output_dir: str):
    total_repos = 0
    repos_with_main_go_mod = 0

    # Count total number of repositories
    with open(input_file, 'r') as csvfile:
        total_repos = sum(1 for row in csv.reader(csvfile) if len(row) == 2)

    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Create a progress bar
        pbar = tqdm(total=total_repos, desc="Processing repositories")
        for row in reader:
            if len(row) == 2:
                owner, repo = row
                repo_name = f"{owner}/{repo}"
                go_mod_files, main_dir_count = get_go_mod_files(owner, repo)
                repos_with_main_go_mod += main_dir_count
                for go_mod in go_mod_files:
                    save_go_mod_file(output_dir, repo_name, go_mod['path'], go_mod['content'])
                pbar.update(1)  # Update progress bar

        pbar.close()  # Close the progress bar

    print(f"\nTotal repositories processed: {total_repos}")
    print(f"Repositories with go.mod in main directory: {repos_with_main_go_mod}")
    print(f"Percentage of repos with go.mod in main directory: {(repos_with_main_go_mod / total_repos) * 100:.2f}%")

if __name__ == "__main__":
    process_repos("data/clients.csv", "go_mod_files")
    print("go.mod files saved in the go_mod_files directory")