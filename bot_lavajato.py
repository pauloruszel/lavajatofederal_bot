from main import main
from logger_config import setup_logging  # <- CORRETO
import logging

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Iniciando execução do bot...")
    main()