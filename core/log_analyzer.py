import re
import os

# ANSI Colors
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_RESET = '\033[0m'

SENSITIVE_PATTERNS = [
    r'\.env',
    r'/\.git/',
    r'wp-config\.php',
    r'/api/v[0-9]+/',
    r'id_rsa'
]

def analyze_logs(filepath):
    if not os.path.exists(filepath):
        print(f"{C_RED}[-] Arquivo não encontrado: {filepath}{C_RESET}")
        return {"error": "File not found"}
        
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        print(f"{C_YELLOW}[!] Acesso suspeito detectado (Linha {line_num}): Padrão '{pattern}'{C_RESET}")
                        findings.append({
                            "line": line_num,
                            "pattern_matched": pattern,
                            "raw_log": line.strip()
                        })
                        
        if not findings:
            print(f"{C_YELLOW}[*] Nenhuma anomalia detectada nos logs.{C_RESET}")
            
        return {
            "target": filepath,
            "type": "Log Analysis",
            "total_anomalies": len(findings),
            "findings": findings
        }
    except Exception as e:
        print(f"{C_RED}[-] Erro ao processar logs: {str(e)}{C_RESET}")
        return {"error": str(e)}
