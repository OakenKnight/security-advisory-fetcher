# Security Advisory Fetcher

This tool fetches security advisories for GitHub repositories and Go modules.

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/security-advisory-fetcher.git
   cd security-advisory-fetcher
   ```

2. Install dependencies using Poetry:

   ```shell
   poetry install
   ```

3. Set up your GitHub token:
   - Create a `.env` file in the project root
   - Add your GitHub token:

     ```shell
     GITHUB_TOKEN=your_github_personal_access_token
     ```

## Usage

The tool can fetch advisories for GitHub repositories or Go modules.

### For GitHub Repositories

```shell
poetry run python -m src.security_advisor.cli --github <owner> <repo>
```

Example:

```shell
poetry run python -m src.security_advisor.cli --github CosmWasm wasmd
```

### For go.mod files

```shell
poetry run python -m src.security_advisor.cli --go-mod <path to file>
```

Example:

```shell
poetry run python -m src.security_advisor.cli --go-mod data/go.mod
```

### For partners scan

```shell
poetry run python -m src.security_advisor.cli --partners-scan
```

This will fetch the go.mod files for all the partners in the data/partners.csv file and save them to go_mod_files directory. Then it will fetch the advisories for each go.mod file and save them to <go.mod file path>/all_mod_vulnerabilities.json
