import logging
from rich.logging import RichHandler

# Mapeamento de prefixos e cores para o Aegis CLI Design System
LOG_PREFIXES = {
    "INFO": "[+] ",
    "SUCCESS": "[✓] ",
    "WARNING": "[!] ",
    "ERROR": "[-] ",
    "CRITICAL": "[-] "
}

class AegisLogFormatter(logging.Formatter):
    def format(self, record):
        log_prefix = LOG_PREFIXES.get(record.levelname, "")
        record.msg = f"{log_prefix}{record.msg}"
        return super().format(record)

def setup_logger(level=logging.INFO):
    """Configura e retorna um logger padronizado com RichHandler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )
    log = logging.getLogger("rich")
    
    # Substitui o formatador padrão pelo nosso customizado
    for handler in log.handlers:
        handler.setFormatter(AegisLogFormatter("%(message)s"))

    # Adiciona um novo nível de log para sucesso
    logging.SUCCESS = 25
    logging.addLevelName(logging.SUCCESS, "SUCCESS")
    
    def success(self, message, *args, **kws):
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, message, args, **kws)
    
    logging.Logger.success = success
    return log

logger = setup_logger()