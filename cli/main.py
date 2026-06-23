import argparse
import sys
import json
from datetime import datetime
from core.config_analyzer import analyze_config
from core.log_analyzer import analyze_logs

# ANSI Colors
C_GREEN = '\033[92m'
C_RED = '\033[91m'
C_BLUE = '\033[94m'
C_YELLOW = '\033[93m'
C_RESET = '\033[0m'

def print_banner():
    print(f"{C_BLUE}╔══════════════════════════════════╗{C_RESET}")
    print(f"{C_BLUE}║         AEGIS FRAMEWORK          ║{C_RESET}")
    print(f"{C_BLUE}║     Static Audit CLI Platform    ║{C_RESET}")
    print(f"{C_BLUE}╚══════════════════════════════════╝{C_RESET}")
    print(f"Version: 1.0.0 | Status: {C_GREEN}Ready{C_RESET}\n")

def save_report(data, report_type):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"reports/aegis_{report_type}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"{C_GREEN}[✓] Relatório salvo em: {filename}{C_RESET}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description='Aegis-Audit: Static Configuration & Log Analyzer')
    parser.add_argument('-c', '--config', help='Caminho para arquivo de configuração (ex: nginx.conf)')
    parser.add_argument('-l', '--log', help='Caminho para arquivo de log de acesso')
    
    args = parser.parse_args()
    
    if not args.config and not args.log:
        print(f"{C_YELLOW}[!] Nenhum alvo fornecido. Use -h para ajuda.{C_RESET}")
        sys.exit(1)
        
    if args.config:
        print(f"{C_BLUE}[+] Iniciando auditoria de configuração em: {args.config}{C_RESET}")
        results = analyze_config(args.config)
        save_report(results, 'config')
        
    if args.log:
        print(f"{C_BLUE}[+] Iniciando análise de logs em: {args.log}{C_RESET}")
        results = analyze_logs(args.log)
        save_report(results, 'logs')

if __name__ == '__main__':
    main()
