import argparse
from .core import fetch_github_advisories, read_partners_csv
from .strategies import GoModStrategy

def main():
    parser = argparse.ArgumentParser(description='Fetch security advisories for GitHub repositories or Go modules.')
    parser.add_argument('--github', nargs=2, metavar=('OWNER', 'REPO'), help='Fetch advisories for a GitHub repository')
    parser.add_argument('--go-mod', type=argparse.FileType('r'), help='Specify the path to a go.mod file to fetch advisories for its dependencies')
    parser.add_argument('--partners-scan', action='store_true', help='Scan partners repositories')
    args = parser.parse_args()

    if args.github:
        owner, repo = args.github
        advisories = fetch_github_advisories(owner, repo)
        print_github_advisories(advisories)
    elif args.go_mod:
        go_mod_content = args.go_mod.read()
        strategy = GoModStrategy()
        advisories = strategy.fetch_advisories(go_mod_content, save_file_location="data/all_mod_vulnerabilities.json")
        print_go_mod_advisories(advisories)
    elif args.partners_scan:
        partners = read_partners_csv("data/partners.csv")
        go_mod_files = []
        for partner in partners:
            strategy = GoModStrategy()
            ret = strategy.fetch_go_mod(partner.owner, partner.name)
            go_mod_files.extend(ret)
        print(go_mod_files)
        for go_mod_file in go_mod_files:
            with open(go_mod_file, 'r') as f:
                go_mod_content = f.read()
                save_vuln_scan_location = '/'.join(go_mod_file.split('/')[:-1])+"/all_mod_vulnerabilities.json"
                advisories = strategy.fetch_advisories(go_mod_content, save_vuln_scan_location)
                print_go_mod_advisories(advisories)
    else:
        parser.print_help()

def print_github_advisories(advisories):
    for advisory in advisories:
        print(f"GHSA ID: {advisory['GHSA ID']}")
        print(f"Title: {advisory['Title']}")
        print(f"Severity: {advisory['Severity']}")
        print(f"Advisory URL: {advisory['Advisory URL']}")
        print("Vulnerabilities:")
        for vuln in advisory['Vulnerabilities']:
            print(f"  Vulnerable Version Range: {vuln['Vulnerable Version Range']}")
            print(f"  Patched Versions: {vuln['Patched Versions']}")
        print("---")

def print_go_mod_advisories(advisories):
    for dep, dep_advisories in advisories.items():
        print(f"Dependency: {dep}")
        print_github_advisories(dep_advisories)
        print("---")

if __name__ == "__main__":
    main()
