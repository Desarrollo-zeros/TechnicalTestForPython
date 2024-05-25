import logging

import logging
import os


def setup_logging():
    log_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../', 'app.log'))

    # Crear un directorio para los logs si no existe
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])
    return logging.getLogger(__name__)


logger = setup_logging()
