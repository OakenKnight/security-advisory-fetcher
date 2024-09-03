import re
from .base_strategy import BaseStrategy
from ..core import fetch_github_advisories

class GoModStrategy(BaseStrategy):
    def fetch_advisories(self, go_mod_content):
        dependencies = self._parse_go_mod(go_mod_content)
        advisories = {}
        for dep in dependencies:
            owner, repo = dep.split('/')[:2]
            advisories[dep] = fetch_github_advisories(owner, repo)
        return advisories

    def _parse_go_mod(self, content):
        dependencies = []
        for line in content.split('\n'):
            match = re.match(r'\s*([^\s]+)\s+v', line)
            if match:
                dependencies.append(match.group(1))
        return dependencies
