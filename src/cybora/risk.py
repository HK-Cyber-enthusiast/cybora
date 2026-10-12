from collections import Counter

from .models import Finding, Severity

WEIGHTS = {
    Severity.CRITICAL: 40,
    Severity.HIGH: 25,
    Severity.MEDIUM: 12,
    Severity.LOW: 4,
    Severity.INFO: 0,
}


def calculate_risk(findings: list[Finding]) -> int:
    """Deterministic score from 0 (no findings) to 100 (very high)."""
    raw = sum(WEIGHTS[f.severity] for f in findings)
    return min(100, raw)


def summary(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(f.severity.value for f in findings)
    return {s.value: counts.get(s.value, 0) for s in Severity}
