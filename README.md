# CYBORA

> **One free security assessment platform. Many assessment modes. One risk picture.**

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-informational.svg)](#testing)
[![Security](https://img.shields.io/badge/security-defensive%20by%20design-orange.svg)](#authorized-use)
[![Status](https://img.shields.io/badge/status-foundation%20release-yellow.svg)](#roadmap)

**Cybora** is a free, modular cybersecurity assessment platform designed to make security assessment useful to everyone—from a student checking a website to a developer reviewing a repository and a security team building an organization-wide assessment workflow.

It combines multiple defensive assessment modules behind one CLI and one normalized finding model.

> **Important:** This repository is an early foundation release. It is intentionally honest about what is implemented now versus what belongs on the roadmap. It does not claim to replace mature enterprise security products.

---

## Table of Contents

- [About](#about)
- [10-Line Description](#10-line-description)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Assessment Modules](#assessment-modules)
- [Examples of Output](#examples-of-output)
- [Reports](#reports)
- [Testing](#testing)
- [Development](#development)
- [Authorized Use](#authorized-use)
- [GitHub Publishing](#github-publishing)
- [AI-Generated Code Verification Checklist](#ai-generated-code-verification-checklist)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## About

Cybora is built around a simple idea:

**Do not make users run ten unrelated security tools and manually interpret the results.**

Instead:

```text
Target
  |
  +--> Web assessment
  +--> Repository assessment
  +--> Dependency assessment
  +--> Local system assessment
  +--> Network exposure assessment
  |
  v
Normalized Findings
  |
  v
Risk Correlation
  |
  v
Prioritized Security Report
```

The platform is local-first. It does not require a paid cloud account or an AI API to perform the foundation assessments.

---

## 10-Line Description

Cybora is a free, modular cybersecurity assessment platform built for everyone.  
It brings multiple defensive security checks into one simple CLI.  
Assess websites, repositories, dependencies, local systems, and network exposure.  
Every module produces the same normalized finding format.  
A risk engine prioritizes findings instead of dumping raw scanner output.  
Reports can be exported as JSON for automation and further analysis.  
The architecture is designed for future cloud, container, API, identity, and compliance modules.  
It is local-first, transparent, and designed to keep sensitive assessment data on the user's machine.  
Safety controls emphasize authorized, non-destructive assessment.  
The long-term goal is a free open security-assessment ecosystem rather than another single-purpose scanner.

---

## Features

### Implemented in this foundation release

- Website security baseline assessment
  - HTTPS/TLS availability
  - Security headers
  - Cookie flags
  - Server disclosure
  - Redirect behavior
  - Basic technology/header observations
- Repository assessment
  - Common hard-coded secret patterns
  - Dangerous code-pattern indicators
  - Risky file names
  - Large/binary-file inventory
- Dependency assessment
  - Python `requirements.txt` / `pyproject.toml` inventory
  - Unpinned dependency detection
  - Basic dependency hygiene findings
- Local system assessment
  - OS/platform information
  - Python/runtime information
  - Environment safety observations
  - Writable working-directory checks
- Local network exposure assessment
  - Explicitly limited to `127.0.0.1` / `localhost` by default
  - Safe connection checks against common local development ports
- Unified severity model
  - Critical / High / Medium / Low / Info
- Deterministic risk scoring
- JSON report export
- Human-readable terminal reports
- Test suite with `pytest`
- Code quality configuration with Ruff
- CI workflow for automated tests
- Clear authorization/safety boundary

### Planned advanced modules

- Attack-surface inventory
- DNS/subdomain inventory for explicitly authorized domains
- API inventory and passive API assessment
- Container/Docker assessment
- IaC assessment for Terraform/Kubernetes
- Cloud posture assessment
- SBOM generation and dependency intelligence
- CVE/KEV/EPSS enrichment
- Attack-path graphing
- Historical posture comparison
- Compliance mapping
- Web dashboard
- Plugin/module SDK
- Continuous monitoring
- SARIF/HTML/PDF reporting
- Optional local AI explanation layer
- Enterprise RBAC and team workspaces

---

## Architecture

Cybora uses a modular pipeline:

```text
                 +-------------------+
                 |      CLI          |
                 +---------+---------+
                           |
                 +---------v---------+
                 | Assessment Runner |
                 +---------+---------+
                           |
       +-------------------+-------------------+
       |          |          |        |        |
       v          v          v        v        v
     Web        Repo       Deps     System   Network
       |          |          |        |        |
       +----------+----------+--------+--------+
                           |
                 +---------v---------+
                 | Finding Normalizer|
                 +---------+---------+
                           |
                 +---------v---------+
                 |   Risk Engine     |
                 +---------+---------+
                           |
                 +---------v---------+
                 | Report Generator  |
                 +-------------------+
```

The important design decision is the **normalized finding model**. Every module emits the same structure, creating a consistent base for future correlation and attack-path analysis across assessment types.

---

## Project Structure

```text
cybora/
├── README.md
├── LICENSE
├── REQUIREMENTS.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   └── cybora/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── models.py
│       ├── runner.py
│       ├── risk.py
│       ├── reporting.py
│       └── modules/
│           ├── __init__.py
│           ├── web.py
│           ├── repo.py
│           ├── dependencies.py
│           ├── system.py
│           └── network.py
└── tests/
    ├── test_risk.py
    ├── test_repo.py
    ├── test_dependencies.py
    └── test_cli.py
```

---

## Requirements

- Python **3.14.4** is the intended target runtime. Validate in a clean Python 3.14.4 environment before publishing a release.
- Python 3.14 is the target runtime for this repository.
- A virtual environment is strongly recommended.
- Internet access is required only for website assessment targets.
- The foundation release does not require Nmap, Docker, a cloud account, or an AI API.

Use a currently supported Python 3.14.x maintenance release when possible; if you stay on 3.14.4, keep the environment isolated and run the full test suite.

---

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/YOUR_USERNAME/cybora.git
cd cybora

py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r REQUIREMENTS.txt
python -m pip install -e .
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
git clone https://github.com/YOUR_USERNAME/cybora.git
cd cybora

py -3.14 -m venv .venv
.venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install -r REQUIREMENTS.txt
python -m pip install -e .
```

### Linux/macOS

```bash
git clone https://github.com/YOUR_USERNAME/cybora.git
cd cybora

python3.14 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r REQUIREMENTS.txt
python -m pip install -e .
```

---

## Quick Start

Check the CLI:

```bash
cybora --help
```

Run a local demo:

```bash
cybora demo
```

Assess a website you own or are authorized to test:

```bash
cybora web https://example.com
```

Assess a repository:

```bash
cybora repo .
```

Assess a dependency file:

```bash
cybora deps REQUIREMENTS.txt
```

Assess the current local machine:

```bash
cybora system
```

Check common local development ports only:

```bash
cybora network
```

Run several defensive assessments and create one JSON report:

```bash
cybora assess --web https://example.com --repo . --deps REQUIREMENTS.txt --system --network --output report.json
```

---

## CLI Usage

### Show version

```bash
cybora --version
```

### Website

```bash
cybora web https://example.com
```

The web module performs non-destructive baseline checks. It does not attempt exploitation.

### Repository

```bash
cybora repo .
```

Use it before publishing a repository to look for common accidental secrets and risky patterns.

### Dependencies

```bash
cybora deps REQUIREMENTS.txt
```

### System

```bash
cybora system
```

### Local network

```bash
cybora network
```

The network module intentionally checks only loopback services in the foundation release.

### Combined assessment

```bash
cybora assess \
  --web https://example.com \
  --repo . \
  --deps REQUIREMENTS.txt \
  --system \
  --network \
  --output cybora-report.json
```

On Windows PowerShell, the same command can be written on one line:

```powershell
cybora assess --web https://example.com --repo . --deps REQUIREMENTS.txt --system --network --output cybora-report.json
```

---

## Assessment Modules

| Module | Current scope | Safety |
|---|---|---|
| `web` | HTTPS, headers, cookies, redirects, disclosure | Read-only/non-destructive |
| `repo` | Secrets/patterns/files | Local analysis |
| `deps` | Dependency hygiene | Local analysis |
| `system` | Local runtime/security observations | Local only |
| `network` | Loopback service exposure | Local only |
| Future `cloud` | Cloud posture | Explicit credentials/scope |
| Future `api` | API inventory/passive checks | Authorized targets only |
| Future `container` | Docker/image configuration | Local analysis |
| Future `compliance` | Framework mappings | Evidence-based |

---

## Examples of Output

Example terminal output:

```text
CYBORA SECURITY ASSESSMENT

Target: repository
Findings: 4
Risk score: 62/100

HIGH    Possible hard-coded credential
        File: config/settings.py
        Evidence: API_KEY assignment pattern

MEDIUM  Unpinned dependency
        File: requirements.txt
        Evidence: requests

LOW     Risky file name
        File: .env.example

INFO    Large binary file
        File: assets/demo.bin

Priority:
1. Review and rotate any real credential.
2. Pin dependencies and review lock/update policy.
3. Keep secrets out of source control.
```

Example JSON structure:

```json
{
  "tool": "cybora",
  "version": "0.1.0",
  "risk_score": 62,
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 1,
    "low": 1,
    "info": 1
  },
  "findings": []
}
```

---

## Reports

JSON reports are intentionally machine-readable.

This enables future integrations with:

- CI/CD
- GitHub Actions
- dashboards
- SIEM pipelines
- ticketing systems
- compliance evidence workflows

Do not upload reports containing secrets or sensitive infrastructure details to public repositories.

---

## Testing

Install development dependencies from `REQUIREMENTS.txt`, then:

```bash
pytest -q
```

Run with coverage:

```bash
pytest --cov=cybora --cov-report=term-missing
```

Run linting:

```bash
ruff check .
```

Format/check:

```bash
ruff format --check .
```

Before a GitHub release, run:

```bash
python -m pip check
pytest -q
ruff check .
ruff format --check .
```

---

## Development

Editable installation:

```bash
python -m pip install -e .
```

Run without installing the CLI entry point:

```bash
python -m cybora --help
```

Add a module by:

1. Creating `src/cybora/modules/<name>.py`.
2. Returning `Finding` objects.
3. Registering the module in the runner/CLI.
4. Adding tests.
5. Documenting it in README.
6. Adding any new dependency to `REQUIREMENTS.txt`.
7. Running the full verification commands.

---

## Authorized Use

Cybora is intended for defensive security assessment.

Only assess:

- systems you own;
- systems where you have explicit permission;
- intentionally provided security-testing targets;
- local systems and repositories you are authorized to inspect.

Do not use the tool to scan third-party infrastructure without authorization.

The foundation release deliberately avoids exploit delivery, credential attacks, destructive actions, persistence, stealth, or automated intrusion.

---

## GitHub Publishing

### 1. Create the repository

On GitHub:

1. Sign in.
2. Select **New repository**.
3. Name it `cybora`.
4. Choose Public if you want the project open source.
5. Do not create a second README if this project already contains one.
6. Do not commit secrets.

### 2. Initialize Git

```bash
git init
git branch -M main
git add .
git commit -m "Initial Cybora foundation release"
```

### 3. Connect GitHub

Replace `YOUR_USERNAME`:

```bash
git remote add origin https://github.com/YOUR_USERNAME/cybora.git
git push -u origin main
```

### 4. Verify the public repository

Check:

- README renders correctly.
- License appears on GitHub.
- No `.venv` folder was committed.
- No `.env` file was committed.
- No API keys/passwords/tokens are present.
- Tests pass.
- GitHub Actions passes.
- Installation commands match `REQUIREMENTS.txt`.
- README commands match the actual CLI.
- Every advertised feature is actually implemented.

### 5. Recommended repository settings

Enable:

- Issues
- Discussions (optional)
- Dependabot
- Secret scanning where available
- Code scanning where available
- Branch protection for `main`
- Pull request reviews once contributors join

---

## AI-Generated Code Verification Checklist

Because this project was generated with AI assistance, **do not publish it blindly**.

### Dependency checks

```bash
python -m pip check
python -m pip list
```

Confirm that every third-party package used by the code is present in `REQUIREMENTS.txt`.

### Import checks

```bash
python -c "import cybora; print(cybora.__version__)"
```

### CLI checks

```bash
cybora --help
cybora --version
cybora demo
```

### Test checks

```bash
pytest -q
```

### Static quality

```bash
ruff check .
ruff format --check .
```

### Security review

Manually inspect:

- subprocess calls
- filesystem writes
- network requests
- URL handling
- redirects
- certificate verification
- user-controlled file paths
- report generation
- logging
- exception handling
- secret handling
- dependency versions

### Functional consistency

Cross-check:

1. README commands against `cli.py`.
2. Module names against `modules/`.
3. Dependency names against imports.
4. Version numbers against `pyproject.toml`.
5. CLI examples against actual output.
6. Tests against implemented behavior.
7. License text against your intended license.
8. GitHub Actions Python version against supported runtime.
9. Roadmap items are not described as implemented.
10. Security claims are not stronger than the tests/evidence.

---

## Roadmap

### Phase 1 — Foundation

- [x] Unified finding model
- [x] CLI
- [x] Web baseline
- [x] Repository analysis
- [x] Dependency hygiene
- [x] Local system assessment
- [x] Local network exposure
- [x] Risk scoring
- [x] JSON reporting
- [x] Tests
- [x] CI

### Phase 2 — Security Intelligence

- [ ] CVE enrichment
- [ ] CISA KEV enrichment
- [ ] EPSS enrichment
- [ ] Technology fingerprinting
- [ ] Asset inventory
- [ ] SBOM
- [ ] SARIF
- [ ] HTML report

### Phase 3 — Advanced Assessment

- [ ] API assessment
- [ ] Container assessment
- [ ] Kubernetes assessment
- [ ] Terraform/IaC assessment
- [ ] Cloud posture
- [ ] Identity assessment
- [ ] Authentication/security-control review
- [ ] Compliance mappings

### Phase 4 — Correlation

- [ ] Finding deduplication
- [ ] Asset graph
- [ ] Attack-path graph
- [ ] Business-impact scoring
- [ ] Historical posture
- [ ] Remediation prioritization

### Phase 5 — Platform

- [ ] Web dashboard
- [ ] Plugin SDK
- [ ] CI/CD integrations
- [ ] Team workspaces
- [ ] RBAC
- [ ] Continuous monitoring
- [ ] Local AI assistant
- [ ] Enterprise deployment options

---

## Contributing

Contributions are welcome.

Good first contributions include:

- tests
- documentation
- new safe assessment modules
- parsers
- report formats
- platform compatibility fixes
- performance improvements

For new security modules, contributors should clearly document:

- scope
- permissions required
- network behavior
- data collected
- safety controls
- expected false positives
- tests
- limitations

Please never submit code that performs unauthorized access, destructive actions, credential theft, persistence, or evasion.

---

## Acknowledgements

Cybora is built using the Python ecosystem and open security knowledge.

The project is designed to complement—not replace—mature tools and standards such as OWASP guidance, NIST publications, CVE/NVD data, CISA KEV, EPSS, SARIF, and established security testing methodologies.

---

## License

Cybora is released under the MIT License. See [LICENSE](LICENSE).

---

## Name Note

The project name **Cybora** is a working name. This is **not** a trademark or legal availability guarantee. Before public branding, verify the name through GitHub, PyPI, package registries, domains, social platforms, and relevant trademark databases.
