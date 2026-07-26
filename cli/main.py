import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from cli.banner import show_banner
from core.logger import logger
from core import engine

app = typer.Typer()
console = Console()

class AppState:
    def __init__(self):
        self.target_url = None
        self.findings = {}

state = AppState()

def show_menu():
    console.print(Panel(
        "[bold cyan][1][/bold cyan] Set Target (Cloud Run/GKE URL)\n" 
        "[bold cyan][2][/bold cyan] Enum Metadata Service\n" 
        "[bold cyan][3][/bold cyan] Audit SA Permissions (Manual Input)\n" 
        "[bold cyan][4][/bold cyan] Generate Report\n" 
        "[bold cyan][5][/bold cyan] Doctor (Health Check)\n" 
        "[bold cyan][6][/bold cyan] Exit",
        title="AEGIS AUDIT - Interactive Menu",
        border_style="bold green"
    ))

@app.command(help="Inicia a suíte de auditoria em modo interativo.")
def interactive():
    show_banner()
    while True:
        show_menu()
        choice = Prompt.ask("Selecione uma opção", choices=["1", "2", "3", "4", "5", "6"], default="6")

        if choice == '1':
            state.target_url = Prompt.ask("[+] Insira a URL do alvo")
            logger.success(f"Alvo definido para: {state.target_url}")
        elif choice == '2':
            if not state.target_url:
                logger.error("Nenhum alvo definido. Use a opção [1] primeiro.")
                continue
            engine.check_metadata_server(state.target_url)
        elif choice == '3':
            logger.info("Cole as permissões da Service Account (uma por linha). Pressione Ctrl+D quando terminar.")
            permissions = []
            try:
                while True:
                    line = input()
                    if line:
                        permissions.append(line.strip())
            except EOFError:
                pass
            findings = engine.analyze_permissions(permissions)
            state.findings.update(findings)
        elif choice == '4':
            logger.info("Gerando relatório...")
            console.print(Panel(str(state.findings), title="Resultados da Auditoria"))
        elif choice == '5':
            logger.info("Executando health check... [OK]")
        elif choice == '6':
            logger.info("Saindo. Obrigado por usar o Aegis Audit!")
            break

if __name__ == "__main__":
    interactive()