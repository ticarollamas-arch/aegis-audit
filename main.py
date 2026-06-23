import argparse
import sys
import json
from core.detector import LogAnalyzer

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_banner():
    banner = f"""{BLUE}
┌──────────────────────────┐
│  AEGIS SECURITY ENGINE   │
├──────────────────────────┤
│ Status: ACTIVE           │
│ Mode:  DEFENSIVE AUDIT   │
│ Module: aegis-audit      │
└──────────────────────────┘
{RESET}"""
    print(banner)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description='Aegis Audit - Web Log Security Analyzer')
    parser.add_argument('-l', '--log', required=True, help='Caminho para o arquivo de log (ex: access.log)')
    parser.add_argument('-f', '--format', choices=['txt', 'json'], default='txt', help='Formato de saída')
    
    args = parser.parse_args()
    
    print(f"{GREEN}[+] Inicializando análise de logs no arquivo: {args.log}{RESET}")
    
    analyzer = LogAnalyzer(args.log)
    try:
        results = analyzer.analyze()
        
        if not results:
            print(f"{GREEN}[✓] Nenhuma anomalia crítica detectada.{RESET}")
            sys.exit(0)
            
        print(f"{YELLOW}[!] Foram detectadas {len(results)} requisições suspeitas.{RESET}")
        
        if args.format == 'json':
            with open('aegis_report.json', 'w') as f:
                json.dump(results, f, indent=4)
            print(f"{GREEN}[✓] Relatório salvo em aegis_report.json{RESET}")
        else:
            with open('aegis_report.txt', 'w') as f:
                for res in results:
                    line = f"[{res['timestamp']}] IP: {res['ip']} | Endpoint: {res['endpoint']} | Risco: {res['risk_score']}\n"
                    f.write(line)
                    print(f"{RED}[-] Ameaça: {res['ip']} tentou acessar {res['endpoint']}{RESET}")
            print(f"{GREEN}[✓] Relatório salvo em aegis_report.txt{RESET}")
            
    except FileNotFoundError:
        print(f"{RED}[-] Erro: Arquivo {args.log} não encontrado.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[-] Erro inesperado: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == '__main__':
    main()
