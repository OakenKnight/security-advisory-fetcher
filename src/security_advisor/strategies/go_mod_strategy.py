import re
import json
from .base_strategy import BaseStrategy
from ..core import fetch_github_advisories
import requests
import os
import base64
from ..utils import load_github_token

class GoModStrategy(BaseStrategy):
    def fetch_go_mod(self, owner, repo_name):
        """
        Fetch go.mod files from a GitHub repository and save them locally.
        
        :param owner: GitHub repository owner
        :param repo_name: GitHub repository name
        :param github_token: GitHub personal access token (optional)
        :return: List of paths to saved go.mod files
        """

        base_url = f"https://api.github.com/repos/{owner}/{repo_name}/git/trees/main?recursive=1"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {load_github_token()}"
        }
        
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        
        tree = response.json()["tree"]
        go_mod_files = [item for item in tree if item["path"].endswith("go.mod")]
        
        saved_files = []
        
        for file in go_mod_files:
            file_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file['path']}"
            file_response = requests.get(file_url, headers=headers)
            file_response.raise_for_status()
            
            content = base64.b64decode(file_response.json()["content"]).decode("utf-8")
            
            # Create a local directory structure
            local_path = os.path.join("go_mod_files", owner, repo_name, file["path"])
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Save the file locally
            with open(local_path, "w") as f:
                f.write(content)
            
            saved_files.append(local_path)
        
        return saved_files

    def fetch_advisories(self, go_mod_content, save_file_location):
        """
        Fetch security advisories for dependencies in a go.mod file.

        :param go_mod_content: Content of the go.mod file as a string
        :return: Dictionary of dependencies and their associated advisories
        """
        dependencies = self._parse_go_mod(go_mod_content)
        all_vulnerabilities = {}

        for dep, version in dependencies.items():
            owner, repo = self._extract_owner_repo(dep)
            if owner and repo:
                advisories = fetch_github_advisories(owner, repo)
                if advisories:
                    all_vulnerabilities[dep] = advisories
        self._save_all_vulnerabilities(all_vulnerabilities, save_file_location)
        return all_vulnerabilities

    def _parse_go_mod(self, content):
        """
        Parse the go.mod file content to extract dependencies and their versions.

        :param content: Content of the go.mod file as a string
        :return: Dictionary of dependencies and their versions
        """
        dependencies = {}
        for line in content.split('\n'):
            match = re.match(r'\s*(github\.com/[^\s]+)\s+(v\d+\.\d+\.\d+)', line)
            if match:
                dependencies[match.group(1)] = match.group(2)
        return dependencies

    def _extract_owner_repo(self, dependency):
        """
        Extract the owner and repository name from a dependency string.

        :param dependency: Dependency string in the format "github.com/owner/repo"
        :return: Tuple containing the owner and repository name
        """
        parts = dependency.split('/')
        if len(parts) >= 3 and parts[0] == 'github.com':
            return parts[1], parts[2]
        return None, None

    def _save_all_vulnerabilities(self, all_vulnerabilities, save_file_location):
        """
        Save all vulnerabilities to a JSON file.

        :param all_vulnerabilities: Dictionary of all vulnerabilities
        """
        with open(save_file_location, 'w') as f:
            json.dump(all_vulnerabilities, f, indent=2)
