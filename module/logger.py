import logging
import logging.handlers

import backtester
import os
from datetime import datetime

class logger():
    logger = None
    
    def __init__(self, name: str, filename: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] >> %(message)s')

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        logFileName = f'{filename}'
        logFilePath = os.path.join(backtester.modpath, '../log', logFileName)

        fileHandler = logging.handlers.RotatingFileHandler(logFilePath, maxBytes=1024*1024*100, backupCount=2)
        fileHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)

        self.logger.info('==================== New log ====================')
