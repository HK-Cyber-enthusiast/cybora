# CYBORA

> **One free security assessment platform. Many assessment modes. One risk picture.**

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cybora.svg)](https://pypi.org/project/cybora/)
[![Security](https://img.shields.io/badge/security-defensive%20by%20design-orange.svg)](#authorized-use)
[![Status](https://img.shields.io/badge/status-foundation%20release-yellow.svg)](#roadmap)

**Cybora** is a free, modular cybersecurity assessment platform designed to bring multiple defensive security checks into one command-line interface (CLI).

It is designed for students, developers, and security teams who want to assess websites, review repositories, inspect dependency files, and examine local system and network exposure.

Cybora uses a unified finding format to help organize assessment results in one place.

> **Note:** Cybora `0.1.0` is an early foundation release. Features should be considered implemented only where supported by the actual code and tests. It is not a replacement for mature enterprise security products.

---

## Table of Contents

* [About](#about)
* [Features](#features)
* [Architecture](#architecture)
* [Requirements](#requirements)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [CLI Commands](#cli-commands)
* [Assessment Modules](#assessment-modules)
* [Example Output](#example-output)
* [Testing](#testing)
* [Development](#development)
* [Authorized Use](#authorized-use)
* [GitHub Publishing](#github-publishing)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)

---

## About

Cybora aims to simplify defensive security assessment by bringing multiple checks into a single CLI.

Instead of running unrelated tools and manually combining their output, Cybora provides a common interface for supported assessment modules.

```text
                  CYBORA CLI
                      |
              Assessment Runner
                      |
          +-----------+-----------+
          |           |           |
         Web         Repo        Deps
          |           |           |
        System      Network       |
          |           |           |
          +-----------+-----------+
                      |
               Security Findings
                      |
                Risk Assessment
                      |
                  Final Report
```

Cybora is designed for local-first use. Its foundation package does not require a paid cloud account or an AI API.

---

## Features

Cybora `0.1.0` provides the following command groups, subject to verification against the actual source code:

* **Web:** Non-destructive website baseline assessment.
* **Repo:** Local repository inspection for common accidental secrets and risky patterns.
* **Deps:** Dependency pinning and source-hygiene assessment.
* **System:** Local system assessment without privileged changes.
* **Network:** Checks common service ports on loopback.
* **Assess:** Combines supported defensive assessments into a report.
* **Demo:** Demonstrates the reporting workflow using sample data.

### Planned capabilities

* Vulnerability intelligence and CVE enrichment
* Software Bill of Materials (SBOM)
* Container and cloud assessments
* API and infrastructure-as-code assessment
* Historical security posture comparisons
* HTML and SARIF reports
* Web dashboard and plugin SDK
* Compliance mappings and finding correlation

These are roadmap items, not promises that they are available in the current release.

---

## Architecture

Cybora is organized around a common assessment workflow:

1. Accept a target or local assessment scope.
2. Run the selected assessment modules.
3. Normalize module findings.
4. Apply available risk-scoring logic.
5. Present findings and supported report formats.

The CLI and module implementations define the actual capabilities of the current release.

---

## Requirements

* Python 3.14 or a compatible supported Python version.
* `pip` for installing the package.
* Internet access for website assessments.
* A virtual environment is recommended for development.

Use the Python version and dependencies specified in the project's packaging configuration.

---

## Installation

### Install from PyPI

Install Cybora using pip:

```powershell
python -m pip install cybora
```

Check the installed version:

```powershell
python -m cybora --version
```

Display available commands:

```powershell
python -m cybora --help
```

### Install from source

Clone the repository:

```powershell
git clone https://github.com/HK-Cyber-enthusiast/cybora.git
cd cybora
```

Create and activate a virtual environment:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Verify the installation:

```powershell
python -m cybora --help
python -m cybora demo
```

---

## Quick Start

### 1. Check the version

```powershell
python -m cybora --version
```

### 2. View available commands

```powershell
python -m cybora --help
```

### 3. Run the demo

```powershell
python -m cybora demo
```

The demo uses sample data and does not represent a real security assessment.

### 4. Inspect a repository

```powershell
python -m cybora repo .
```

Review the findings before publishing code.

### 5. Review dependencies

```powershell
python -m cybora deps REQUIREMENTS.txt
```

Use the actual dependency-file path in your project.

### 6. Assess a website

```powershell
python -m cybora web https://example.com
```

Only assess websites you own or are authorized to test.

### 7. Assess your local system

```powershell
python -m cybora system
```

### 8. Check local network exposure

```powershell
python -m cybora network
```

The foundation release is intended to limit these checks to loopback addresses such as `127.0.0.1` and `localhost`.

---

## CLI Commands

| Command                                    | Purpose                       |
| ------------------------------------------ | ----------------------------- |
| `python -m cybora --help`                  | Display available commands    |
| `python -m cybora --version`               | Display the installed version |
| `python -m cybora demo`                    | Run the sample demonstration  |
| `python -m cybora web https://example.com` | Assess a website baseline     |
| `python -m cybora repo .`                  | Inspect a local repository    |
| `python -m cybora deps REQUIREMENTS.txt`   | Review dependency hygiene     |
| `python -m cybora system`                  | Assess the local system       |
| `python -m cybora network`                 | Check local service exposure  |

### Combined assessment

If supported by the installed version, a combined assessment may look like this:

```powershell
python -m cybora assess --web https://example.com --repo . --deps REQUIREMENTS.txt --system --network --output report.json
```

Check `python -m cybora assess --help` to confirm the available options.

---

## Assessment Modules

| Module    | Purpose                    | Scope                  |
| --------- | -------------------------- | ---------------------- |
| `demo`    | Demonstration findings     | Sample data            |
| `web`     | Website baseline checks    | Authorized website     |
| `repo`    | Repository inspection      | Local files            |
| `deps`    | Dependency hygiene         | Local dependency files |
| `system`  | System observations        | Local machine          |
| `network` | Common service-port checks | Loopback only          |
| `assess`  | Combined assessment        | Supported modules      |

Cybora does not claim that baseline checks identify every vulnerability in a target.

---

## Example Output

Run the demo:

```powershell
python -m cybora demo
```

Illustrative JSON output:

```json
{
  "tool": "cybora",
  "version": "0.1.0",
  "findings": [
    {
      "module": "demo",
      "title": "Sample medium-risk finding",
      "severity": "medium",
      "description": "This is a demonstration finding.",
      "target": "demo://local",
      "remediation": "Replace the demo with a real authorized assessment."
    }
  ]
}
```

This is illustrative output only. Actual output depends on the installed implementation.

---

## Testing

Run these commands from the project directory.

### Check dependencies

```powershell
python -m pip check
```

### Check the Python import

```powershell
python -c "import cybora; print('Cybora Python import works')"
```

### Check the CLI

```powershell
python -m cybora --help
python -m cybora --version
python -m cybora demo
```

### Run tests

If pytest and the project's tests are installed:

```powershell
python -m pytest -q
```

### Run Ruff checks

If Ruff is installed:

```powershell
python -m ruff check .
python -m ruff format --check .
```

Do not claim the tests pass until you have run them and confirmed the results.

---

## Development

Install the local project in editable mode:

```powershell
python -m pip install -e .
```

When contributing a new assessment module:

1. Follow the existing module structure.
2. Use the project's finding model.
3. Add tests for new behavior.
4. Document the module's scope and limitations.
5. Update dependency files when adding packages.
6. Run the relevant tests and quality checks.

---

## Authorized Use

Cybora is intended for lawful, defensive security assessment.

Only assess:

* Systems you own.
* Systems for which you have explicit authorization.
* Local repositories and machines you are permitted to inspect.
* Intentionally provided security-testing targets.

Do not scan or test third-party systems without authorization.

Always review assessment scope, network behavior, and findings before taking action.

---

## GitHub Publishing

**GitHub repository:**
https://github.com/HK-Cyber-enthusiast/cybora

To publish README changes, open PowerShell in your local Cybora project directory.

Check the working tree:

```powershell
git status
```

Stage the README:

```powershell
git add README.md
```

Commit the change:

```powershell
git commit -m "Update Cybora README documentation"
```

Push changes:

```powershell
git push
```

If this is your first push and the remote has not been configured, run:

```powershell
git remote add origin https://github.com/HK-Cyber-enthusiast/cybora.git
git branch -M main
git push -u origin main
```

If `origin` already exists, do not add it again.

Before publishing, check that you have not committed passwords, API keys, access tokens, private reports, or other sensitive files.

---

## Roadmap

### Foundation

* [x] CLI entry point
* [x] Package publication on PyPI
* [ ] Verify every assessment module with automated tests
* [ ] Confirm README examples against the installed CLI
* [ ] Validate the GitHub Actions workflow

### Security Intelligence

* [ ] CVE and vulnerability intelligence
* [ ] CISA KEV and EPSS enrichment
* [ ] SBOM generation
* [ ] Additional report formats

### Advanced Assessment

* [ ] API assessment
* [ ] Container and infrastructure-as-code assessment
* [ ] Cloud security posture
* [ ] Compliance mappings

### Platform

* [ ] Web dashboard
* [ ] Plugin SDK
* [ ] Historical posture tracking
* [ ] Additional CI/CD integrations

Roadmap items should be marked complete only after implementation and verification.

---

## Contributing

Contributions are welcome.

Useful contributions include:

* Bug fixes and automated tests
* Documentation improvements
* Defensive assessment modules
* Report-format improvements
* Python compatibility fixes
* Performance improvements

New security modules should document their scope, permissions, network behavior, collected data, safety controls, expected false positives, and limitations.

---

## Acknowledgements

Cybora uses the Python ecosystem and open security knowledge to support defensive security assessment.

It is intended to complement established security tools and guidance, not replace them.

---

## License

Cybora is released under the MIT License. See [LICENSE](LICENSE) for the full license text.

---

**Cybora 0.1.0 — An early foundation for modular defensive security assessment.**
