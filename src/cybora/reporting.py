from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .models import AssessmentResult

console = Console()


def print_result(result: AssessmentResult) -> None:
    console.print("\n[bold]CYBORA SECURITY ASSESSMENT[/bold]\n")
    console.print(f"Target: {result.target}")
    console.print(f"Findings: {len(result.findings)}")
    console.print(f"Risk score: {result.risk_score}/100\n")

    if not result.findings:
        console.print("[green]No findings in the selected checks.[/green]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Severity")
    table.add_column("Module")
    table.add_column("Finding")
    table.add_column("Target")

    for finding in sorted(result.findings, key=lambda x: _rank(x.severity.value)):
        table.add_row(
            finding.severity.value.upper(),
            finding.module,
            finding.title,
            finding.target,
        )

    console.print(table)
    console.print("\n[bold]Priority guidance[/bold]")
    for i, finding in enumerate(
        sorted(result.findings, key=lambda x: _rank(x.severity.value))[:5], start=1
    ):
        console.print(f"{i}. {finding.title}: {finding.remediation or 'Review manually.'}")


def write_json(result: AssessmentResult, path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(result.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )


def _rank(severity: str) -> int:
    return {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
        "info": 4,
    }.get(severity, 5)
