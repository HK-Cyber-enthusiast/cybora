from __future__ import annotations

from urllib.parse import urlparse

import httpx

from ..models import Finding, Severity

SECURITY_HEADERS = {
    "strict-transport-security": (
        Severity.MEDIUM,
        "Missing HSTS",
        "Consider Strict-Transport-Security for HTTPS deployments after validating deployment behavior.",
    ),
    "content-security-policy": (
        Severity.MEDIUM,
        "Missing Content-Security-Policy",
        "Deploy a carefully tested Content-Security-Policy appropriate to the application.",
    ),
    "x-content-type-options": (
        Severity.LOW,
        "Missing X-Content-Type-Options",
        "Set X-Content-Type-Options: nosniff where appropriate.",
    ),
    "referrer-policy": (
        Severity.LOW,
        "Missing Referrer-Policy",
        "Set a deliberate Referrer-Policy suitable for your application.",
    ),
    "permissions-policy": (
        Severity.INFO,
        "Missing Permissions-Policy",
        "Review whether browser feature permissions should be restricted.",
    ),
}


def scan(url: str) -> list[Finding]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return [
            Finding(
                module="web",
                title="Invalid web target",
                severity=Severity.HIGH,
                description="The supplied value is not a valid HTTP(S) URL.",
                target=url,
                remediation="Use a URL such as https://example.com.",
            )
        ]

    findings = []
    try:
        with httpx.Client(
            follow_redirects=True,
            timeout=8.0,
            verify=True,
            headers={"User-Agent": "Cybora/0.1 defensive-assessment"},
        ) as client:
            response = client.get(url)
    except httpx.HTTPError as exc:
        return [
            Finding(
                module="web",
                title="Web target could not be reached",
                severity=Severity.HIGH,
                description="The HTTP client could not complete a connection.",
                target=url,
                evidence=str(exc)[:300],
                remediation="Verify the URL, connectivity, DNS, and authorization to assess the target.",
            )
        ]

    final_url = str(response.url)
    if parsed.scheme == "http" and urlparse(final_url).scheme != "https":
        findings.append(
            Finding(
                module="web",
                title="HTTP target did not end on HTTPS",
                severity=Severity.HIGH,
                description="The requested HTTP URL did not redirect to HTTPS.",
                target=url,
                remediation="Prefer HTTPS and configure a deliberate HTTP-to-HTTPS redirect.",
            )
        )

    headers = {k.lower(): v for k, v in response.headers.items()}
    for header, (severity, title, remediation) in SECURITY_HEADERS.items():
        if header not in headers:
            findings.append(
                Finding(
                    module="web",
                    title=title,
                    severity=severity,
                    description=f"The response did not include the {header} header.",
                    target=final_url,
                    remediation=remediation,
                )
            )

    server = headers.get("server")
    if server:
        findings.append(
            Finding(
                module="web",
                title="Server header disclosed",
                severity=Severity.LOW,
                description="The HTTP response discloses a server identification header.",
                target=final_url,
                evidence=server[:120],
                remediation="Consider whether detailed server identification is necessary.",
            )
        )

    set_cookie = headers.get("set-cookie", "")
    if set_cookie:
        lower = set_cookie.lower()
        if "secure" not in lower and urlparse(final_url).scheme == "https":
            findings.append(
                Finding(
                    module="web",
                    title="Cookie without Secure attribute observed",
                    severity=Severity.MEDIUM,
                    description="A Set-Cookie response did not visibly include the Secure attribute.",
                    target=final_url,
                    remediation="Use Secure on cookies carrying sensitive session state over HTTPS.",
                )
            )
        if "httponly" not in lower:
            findings.append(
                Finding(
                    module="web",
                    title="Cookie without HttpOnly attribute observed",
                    severity=Severity.LOW,
                    description="A Set-Cookie response did not visibly include HttpOnly.",
                    target=final_url,
                    remediation="Use HttpOnly for cookies that do not need JavaScript access.",
                )
            )

    findings.append(
        Finding(
            module="web",
            title="HTTP response observed",
            severity=Severity.INFO,
            description="A non-destructive HTTP request completed.",
            target=final_url,
            evidence=f"status={response.status_code}; content-type={headers.get('content-type', 'unknown')}",
            remediation="Use the findings above as a baseline; application security requires deeper authorized testing.",
        )
    )

    return findings
