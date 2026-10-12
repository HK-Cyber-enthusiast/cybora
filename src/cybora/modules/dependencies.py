from __future__ import annotations

import re
from pathlib import Path

from ..models import Finding, Severity

PINNED = re.compile(r"^[A-Za-z0-9_.-]+\s*(==|===|~=)\s*[^#\s]+$")


def scan(path: str) -> list[Finding]:
    file = Path(path).resolve()
    if not file.exists():
        return [
            Finding(
                module="deps",
                title="Dependency file does not exist",
                severity=Severity.HIGH,
                description="The supplied dependency file was not found.",
                target=str(file),
                remediation="Provide an existing requirements or dependency file.",
            )
        ]

    findings = []
    for line_no, raw in enumerate(file.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        if line.startswith(("git+", "http://", "https://")):
            findings.append(
                Finding(
                    module="deps",
                    title="Direct URL dependency",
                    severity=Severity.MEDIUM,
                    description="A dependency is sourced directly from a URL instead of a normal package index.",
                    target=f"{file.name}:{line_no}",
                    evidence=line[:160],
                    remediation="Prefer a trusted package release or a reviewed immutable source reference.",
                )
            )
        elif not PINNED.match(line):
            package = re.split(r"[<>=!~\s]", line, maxsplit=1)[0]
            findings.append(
                Finding(
                    module="deps",
                    title="Unpinned dependency",
                    severity=Severity.LOW,
                    description="The dependency does not use an exact or compatible version constraint.",
                    target=f"{file.name}:{line_no}",
                    evidence=package,
                    remediation="Pin or constrain production dependencies and maintain a reviewed update process.",
                )
            )
    return findings
