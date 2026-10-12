from __future__ import annotations

import socket

from ..models import Finding, Severity

COMMON_LOCAL_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3000: "Node development server",
    5000: "Development server",
    8000: "Python development server",
    8080: "HTTP development/proxy",
    8443: "HTTPS development server",
}


def scan(host: str = "127.0.0.1") -> list[Finding]:
    findings = []
    for port, label in COMMON_LOCAL_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.15)
        try:
            is_open = sock.connect_ex((host, port)) == 0
        except OSError:
            is_open = False
        finally:
            sock.close()

        if is_open:
            severity = Severity.LOW if port in {3000, 5000, 8000, 8080, 8443} else Severity.INFO
            findings.append(
                Finding(
                    module="network",
                    title=f"Local service reachable: {label}",
                    severity=severity,
                    description="A common service port accepted a TCP connection on the loopback interface.",
                    target=f"{host}:{port}",
                    remediation="Confirm the service is intentional and appropriately protected. Do not expose development services to untrusted networks.",
                )
            )
    return findings
