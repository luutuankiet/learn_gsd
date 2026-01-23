import shutil
import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

@app.command()
def main(force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files")):
    """
    Initialize GSD-Lite in the current directory.
    """
    # 1. Locate the bundled templates
    # We look for the 'template' folder relative to this script
    package_dir = Path(__file__).parent
    source_dir = package_dir / "template"
    
    # 2. Define destination
    cwd = Path.cwd()
    dest_dir = cwd / "gsd_lite"

    console.print(Panel.fit("[bold cyan]GSD-Lite Scaffolder[/bold cyan]", border_style="cyan"))

    # 3. Validation
    if not source_dir.exists():
        console.print(f"[bold red]Error:[/bold red] Template directory not found at {source_dir}")
        console.print("This usually means the package was built incorrectly.")
        raise typer.Exit(code=1)

    if dest_dir.exists() and not force:
        console.print(f"[yellow]Warning:[/yellow] Directory [bold]{dest_dir}[/bold] already exists.")
        console.print("Use [bold]--force[/bold] to overwrite.")
        raise typer.Exit(code=1)

    # 4. Copying
    try:
        if dest_dir.exists() and force:
            shutil.rmtree(dest_dir)
        
        shutil.copytree(source_dir, dest_dir)
        
        # 5. Success
        console.print(f"[green]✔ Successfully initialized GSD-Lite in:[/green] {dest_dir}")
        console.print("\n[bold]Next Steps:[/bold]")
        console.print("1. Read [bold]gsd_lite/PROTOCOL.md[/bold]")
        console.print("2. Start your first session!")
        
    except Exception as e:
        console.print(f"[bold red]Error copying files:[/bold red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
