import re
import json
from .base_strategy import BaseStrategy
from ..core import fetch_github_advisories

class GoModStrategy(BaseStrategy):
    def fetch_go_mods(self, owner, repo_name):
        pass

    def fetch_advisories(self, go_mod_content):
        dependencies = self._parse_go_mod(go_mod_content)
        all_vulnerabilities = {}

        for dep, version in dependencies.items():
            owner, repo = self._extract_owner_repo(dep)
            if owner and repo:
                advisories = fetch_github_advisories(owner, repo)
                if advisories:
                    all_vulnerabilities[dep] = advisories
        self._save_all_vulnerabilities(all_vulnerabilities)
        return all_vulnerabilities

    def _parse_go_mod(self, content):
        dependencies = {}
        for line in content.split('\n'):
            match = re.match(r'\s*(github\.com/[^\s]+)\s+(v\d+\.\d+\.\d+)', line)
            if match:
                dependencies[match.group(1)] = match.group(2)
        return dependencies

    def _extract_owner_repo(self, dependency):
        parts = dependency.split('/')
        if len(parts) >= 3 and parts[0] == 'github.com':
            return parts[1], parts[2]
        return None, None

    def _save_all_vulnerabilities(self, all_vulnerabilities):
        with open('data/all_mod_vulnerabilities.json', 'w') as f:
            json.dump(all_vulnerabilities, f, indent=2)
