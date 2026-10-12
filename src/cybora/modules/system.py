from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

from ..models import Finding, Severity


def scan() -> list[Finding]:
    findings = [
        Finding(
            module="system",
            title="Runtime inventory",
            severity=Severity.INFO,
            description="Basic local runtime information was collected for the report.",
            target=platform.node() or "localhost",
            evidence=f"OS={platform.platform()} | Python={sys.version.split()[0]}",
            remediation="Keep the operating system and runtime on supported security-maintained versions.",
        )
    ]

    if os.name == "nt":
        findings.append(
            Finding(
                module="system",
                title="Windows local security review reminder",
                severity=Severity.INFO,
                description="The foundation release does not attempt privileged Windows security configuration changes.",
                target=platform.node() or "localhost",
                remediation="Review Windows Update, Defender, firewall, disk encryption, account protection, and least privilege using your organization's baseline.",
            )
        )
    else:
        findings.append(
            Finding(
                module="system",
                title="Local permissions review reminder",
                severity=Severity.INFO,
                description="The foundation release avoids privileged host changes.",
                target=str(Path.home()),
                remediation="Review account privileges, updates, firewall configuration, SSH access, and sensitive file permissions.",
            )
        )
    return findings
