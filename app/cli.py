from contextlib import contextmanager
from typing import Iterator

import typer
from botocore.exceptions import BotoCoreError, ClientError
from rich.console import Console
from rich.table import Table

from app.services.asg_service import AutoScalingService
from app.utils.logger import logger

app = typer.Typer(help="Control a GPU Auto Scaling Group with boto3.")
console = Console()


def get_service() -> AutoScalingService:
    return AutoScalingService()


@contextmanager
def handle_cli_errors() -> Iterator[None]:
    """Turn config/AWS errors into a clean CLI message instead of a traceback."""
    try:
        yield
    except (RuntimeError, BotoCoreError, ClientError) as exc:
        logger.error(str(exc))
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1)


@app.command()
def status() -> None:
    """Show the configured Auto Scaling Group status."""
    with handle_cli_errors():
        asg_status = get_service().get_asg_status()

        table = Table(title="GPU Auto Scaling Group")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        for key, value in asg_status.items():
            table.add_row(key.replace("_", " ").title(), str(value))

        console.print(table)


@app.command()
def start(
    desired_capacity: int = typer.Option(
        1,
        "--desired-capacity",
        "-d",
        help="Desired GPU instance count to request.",
    ),
) -> None:
    """Start GPU capacity by raising desired and minimum capacity."""
    if desired_capacity < 1:
        raise typer.BadParameter("desired capacity must be at least 1")

    with handle_cli_errors():
        get_service().start_gpu(desired_capacity=desired_capacity)
        console.print(
            f"Requested GPU ASG start with desired capacity {desired_capacity}."
        )


@app.command()
def stop() -> None:
    """Stop GPU capacity by setting desired and minimum capacity to zero."""
    with handle_cli_errors():
        get_service().stop_gpu()
        console.print("Requested GPU ASG stop with desired capacity 0.")
