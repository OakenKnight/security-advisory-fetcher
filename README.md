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
