from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Severity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Finding(BaseModel):
    module: str
    title: str
    severity: Severity
    description: str
    target: str
    evidence: str | None = None
    remediation: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AssessmentResult(BaseModel):
    tool: str = "cybora"
    version: str
    target: str
    findings: list[Finding] = Field(default_factory=list)
    risk_score: int = 0
