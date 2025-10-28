import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    """Configure le système de logging."""
    # Créer le dossier logs s'il n'existe pas
    os.makedirs('logs', exist_ok=True)
    
    # Logger principal
    logger = logging.getLogger('pizzeria')
    logger.setLevel(logging.INFO)
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s - %(message)s'
    )
    
    # Handler pour fichier avec rotation quotidienne
    file_handler = TimedRotatingFileHandler(
        'logs/app.log',
        when='midnight',
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Ajouter les handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Instance globale du logger
logger = setup_logging()
