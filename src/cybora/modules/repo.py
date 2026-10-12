from __future__ import annotations

import re
from pathlib import Path

from ..models import Finding, Severity

SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "Generic API key assignment",
        re.compile(r"(?i)\b(api[_-]?key|secret[_-]?key)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    ),
    ("Private key marker", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    (
        "Generic password assignment",
        re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    ),
]

RISKY_NAMES = {".env", "id_rsa", "id_ed25519", "credentials.json", "secrets.json"}


def scan(path: str) -> list[Finding]:
    root = Path(path).resolve()
    findings: list[Finding] = []

    if not root.exists():
        return [
            Finding(
                module="repo",
                title="Repository path does not exist",
                severity=Severity.HIGH,
                description="The requested repository path could not be found.",
                target=str(root),
                remediation="Check the path and run the assessment again.",
            )
        ]

    for file in _files(root):
        rel = str(file.relative_to(root))
        if file.name in RISKY_NAMES:
            findings.append(
                Finding(
                    module="repo",
                    title="Sensitive-looking file present",
                    severity=Severity.MEDIUM,
                    description="A file commonly used for credentials or secrets exists in the repository.",
                    target=rel,
                    remediation="Verify it contains no real secrets and keep credential files out of version control.",
                )
            )

        if file.stat().st_size > 25 * 1024 * 1024:
            findings.append(
                Finding(
                    module="repo",
                    title="Very large file",
                    severity=Severity.LOW,
                    description="Large files can increase repository exposure and supply-chain review burden.",
                    target=rel,
                    evidence=f"{file.stat().st_size} bytes",
                    remediation="Use an appropriate artifact store or Git LFS when justified.",
                )
            )

        if file.suffix.lower() not in {
            ".py",
            ".js",
            ".ts",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".ini",
            ".env",
            ".txt",
            ".md",
        }:
            continue

        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(
                    Finding(
                        module="repo",
                        title=f"Possible {label}",
                        severity=Severity.HIGH,
                        description="A heuristic pattern resembling a credential or private key was found.",
                        target=rel,
                        remediation="Inspect the exact line, remove real secrets, rotate exposed credentials, and use a secret manager.",
                    )
                )

        if re.search(r"(?m)^\s*eval\s*\(", text):
            findings.append(
                Finding(
                    module="repo",
                    title="Dynamic eval usage",
                    severity=Severity.MEDIUM,
                    description="Dynamic evaluation can increase code-injection risk depending on data flow.",
                    target=rel,
                    remediation="Avoid eval where possible and validate untrusted input before any dynamic execution.",
                )
            )

    return _dedupe(findings)


def _files(root: Path):
    ignored = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache"}
    for p in root.rglob("*"):
        if p.is_file() and not any(part in ignored for part in p.parts):
            yield p


def _dedupe(findings: list[Finding]) -> list[Finding]:
    seen = set()
    result = []
    for f in findings:
        key = (f.module, f.title, f.target)
        if key not in seen:
            seen.add(key)
            result.append(f)
    return result
