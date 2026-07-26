import requests
from typing import Dict, Any, Optional
from core.logger import logger

METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/"
METADATA_HEADERS = {"Metadata-Flavor": "Google"}

# Permissões perigosas conhecidas no GCP IAM
DANGEROUS_PERMISSIONS = {
    "iam.serviceAccounts.actAs": "Permite impersonar outra Service Account.",
    "iam.serviceAccountKeys.create": "Permite criar chaves para uma Service Account.",
    "resourcemanager.projects.setIamPolicy": "Permite alterar políticas de IAM no nível do projeto.",
    "storage.buckets.setIamPolicy": "Permite alterar políticas de IAM em buckets do GCS.",
    "iam.roles.update": "Permite modificar roles de IAM existentes."
}

def check_metadata_server(target_url: str) -> bool:
    """Verifica se o metadata server do GCP está acessível a partir de um alvo.
       Esta é uma simulação passiva, na prática seria uma tentativa de SSRF.
    """
    logger.info(f"Iniciando verificação do Metadata Service para o alvo: {target_url}")
    logger.info("Este é um teste conceitual. Uma vulnerabilidade de SSRF seria necessária para explorar isso.")
    logger.info(f"Tentando acessar o endpoint padrão: {METADATA_URL}")

    try:
        # Em um cenário real, o 'target_url' seria vulnerável a SSRF e usado para fazer esta requisição.
        # Aqui, fazemos uma requisição direta para simular o que aconteceria.
        # Nota: Este comando só funcionará se executado de dentro de uma VM/contêiner GCP.
        response = requests.get(METADATA_URL, headers=METADATA_HEADERS, timeout=5.0)
        
        if response.status_code == 200 and 'computeMetadata/' in response.text:
            logger.success("O Metadata Service parece estar acessível a partir deste ambiente.")
            logger.warning("ALERTA: Se um SSRF existir no alvo, um atacante pode obter tokens de SA.")
            return True
        else:
            logger.error(f"Falha ao acessar o Metadata Service. Status: {response.status_code}")
            return False

    except requests.exceptions.Timeout:
        logger.error("Falha ao conectar ao Metadata Service: Timeout excedido.")
        return False
    except requests.exceptions.ConnectionError:
        logger.error("Falha ao conectar ao Metadata Service: Conexão recusada. (Provavelmente não está em um ambiente GCP)")
        return False
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erro HTTP ao acessar o Metadata Service: {http_err}")
        return False
    except Exception as e:
        logger.error(f"Um erro inesperado ocorreu: {e}")
        return False

def analyze_permissions(permissions: list) -> Dict[str, str]:
    """Analisa uma lista de permissões de IAM e retorna as que são perigosas."""
    logger.info(f"Analisando {len(permissions)} permissões...")
    findings = {}
    for perm in permissions:
        if perm in DANGEROUS_PERMISSIONS:
            findings[perm] = DANGEROUS_PERMISSIONS[perm]
            logger.warning(f"Permissão perigosa encontrada: {perm} - {findings[perm]}")
    
    if not findings:
        logger.success("Nenhuma permissão perigosa conhecida encontrada.")
        
    return findings