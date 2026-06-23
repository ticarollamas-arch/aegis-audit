import re
import os

# ANSI Colors
C_GREEN = '\033[92m'
C_RED = '\033[91m'
C_RESET = '\033[0m'

SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Frame-Options',
    'X-Content-Type-Options'
]

def analyze_config(filepath):
    if not os.path.exists(filepath):
        print(f"{C_RED}[-] Arquivo não encontrado: {filepath}{C_RESET}")
        return {"error": "File not found"}
        
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for header in SECURITY_HEADERS:
            # Busca simples por diretivas de adição de header (ex: add_header X-Frame-Options)
            pattern = re.compile(rf'add_header\s+{header}', re.IGNORECASE)
            if pattern.search(content):
                print(f"{C_GREEN}[✓] Cabeçalho encontrado: {header}{C_RESET}")
                findings.append({"header": header, "status": "Present"})
            else:
                print(f"{C_RED}[!] Cabeçalho ausente: {header}{C_RESET}")
                findings.append({"header": header, "status": "Missing"})
                
        return {
            "target": filepath,
            "type": "Configuration Audit",
            "findings": findings
        }
    except Exception as e:
        print(f"{C_RED}[-] Erro ao ler arquivo: {str(e)}{C_RESET}")
        return {"error": str(e)}
