from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .modules import dependencies, network, repo as repo_module, system, web as web_module
from .reporting import print_result, write_json
from .runner import build_result

app = typer.Typer(
    name="cybora",
    help="Free modular defensive cybersecurity assessment platform.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=lambda value: _version_callback(value), is_eager=True
    ),
):
    """Cybora CLI entry point."""
    return None


def _version_callback(value: bool):
    if value:
        typer.echo(f"cybora {__version__}")
        raise typer.Exit()


@app.command()
def demo():
    """Run a safe local demo using an in-memory sample."""
    sample = [
        {
            "module": "demo",
            "title": "Sample medium-risk finding",
            "severity": "medium",
            "description": "This is a demonstration finding.",
            "target": "demo://local",
            "remediation": "Replace the demo with a real authorized assessment.",
        }
    ]
    console.print_json(json.dumps({"tool": "cybora", "version": __version__, "findings": sample}))


@app.command()
def web(target: str):
    """Run a non-destructive website baseline assessment."""
    result = build_result(target, web_module.scan(target))
    print_result(result)



@app.command()
def repo(target: str = typer.Argument(".", help="Repository directory.")):
    """Scan a local repository for common accidental secrets and risky patterns."""
    result = build_result(target, repo_module.scan(target))
    print_result(result)


@app.command("deps")
def deps_command(target: str = typer.Argument(..., help="Dependency file.")):
    """Assess dependency pinning and source hygiene."""
    result = build_result(target, dependencies.scan(target))
    print_result(result)


@app.command("system")
def system_assess():
    """Assess the local system without making privileged changes."""
    result = build_result("local-system", system.scan())
    print_result(result)


@app.command("network")
def network_assess():
    """Check common service ports on loopback only."""
    result = build_result("127.0.0.1", network.scan())
    print_result(result)


@app.command()
def assess(
    web_target: Optional[str] = typer.Option(None, "--web", help="Authorized HTTP(S) target."),
    repo_target: Optional[str] = typer.Option(None, "--repo", help="Local repository."),
    deps_target: Optional[str] = typer.Option(None, "--deps", help="Dependency file."),
    system_check: bool = typer.Option(False, "--system", help="Include local system assessment."),
    network_check: bool = typer.Option(False, "--network", help="Include loopback network assessment."),
    output: Optional[str] = typer.Option(None, "--output", help="Write JSON report to this path."),
):
    """Run multiple defensive assessments and combine findings into one report."""
    findings = []
    targets = []

    if web_target:
        findings.extend(web_module.scan(web_target))
        targets.append(f"web:{web_target}")
    if repo_target:
        findings.extend(repo_module.scan(repo_target))
        targets.append(f"repo:{repo_target}")
    if deps_target:
        findings.extend(dependencies.scan(deps_target))
        targets.append(f"deps:{deps_target}")
    if system_check:
        findings.extend(system.scan())
        targets.append("system:local")
    if network_check:
        findings.extend(network.scan())
        targets.append("network:loopback")

    if not targets:
        raise typer.BadParameter("Choose at least one assessment option.")

    result = build_result(" | ".join(targets), findings)
    print_result(result)

    if output:
        write_json(result, output)
        console.print(f"\n[green]JSON report written to {Path(output).resolve()}[/green]")


if __name__ == "__main__":
    app()
