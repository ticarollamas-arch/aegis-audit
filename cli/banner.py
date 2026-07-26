from rich.console import Console
from rich.panel import Panel
from rich.align import Align

console = Console()

BANNER_ASCII = """
    _    _             _     _   _ _   _ _ 
   / \  | | ____ _ ___(_) __| | | | | | | |
  / _ \ | |/ / _` / __| |/ _` | | | | | | |
 / ___ \|   < (_| \__ \ | (_| | |_| |_|_|_|
/_/   \_\_|\_\__,_|___/_|\__,_|\___/(_|_|_)
              GCP AUDIT SUITE
"""

def show_banner():
    """Exibe o banner de inicialização da ferramenta."""
    panel_content = (
        f"{BANNER_ASCII}\n\n"
        "[bold]Version:[/] 1.0.0\n"
        "[bold]Plugins:[/] 1 Loaded (gcp_escalation_paths)\n"
        "[bold]Status:[/] [green]Ready[/green]"
    )
    
    panel = Panel(
        Align.center(panel_content, vertical="middle"),
        title="AEGIS FRAMEWORK",
        subtitle="Enterprise CLI Platform",
        border_style="bold blue"
    )
    console.print(panel)
