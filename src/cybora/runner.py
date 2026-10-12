from __future__ import annotations

from . import __version__
from .models import AssessmentResult, Finding
from .risk import calculate_risk


def build_result(target: str, findings: list[Finding]) -> AssessmentResult:
    return AssessmentResult(
        version=__version__,
        target=target,
        findings=findings,
        risk_score=calculate_risk(findings),
    )
