from cybora.models import Finding, Severity
from cybora.risk import calculate_risk


def make(severity):
    return Finding(
        module="test",
        title="x",
        severity=severity,
        description="x",
        target="x",
    )


def test_empty_risk_is_zero():
    assert calculate_risk([]) == 0


def test_risk_is_capped():
    assert (
        calculate_risk([make(Severity.CRITICAL), make(Severity.CRITICAL), make(Severity.HIGH)])
        == 100
    )
