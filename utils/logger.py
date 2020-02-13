import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, logging_target: str, filaname=None):
        format = "%(asctime)s: %(message)s"

        if logging_target == "CONSOLE":
            logging.basicConfig(format=format, level=logging.INFO,
                                datefmt="%H:%M:%S")

        elif logging_target == "CSV":


            today = datetime.now()
            cwd = os.getcwd()
            cwd = os.path.split(cwd)[0] + "/Logs/"

            try:
                logging.basicConfig(filename=cwd + "/" + today.strftime("%d_%m_%Y_%H_%M_%S") + ".log",
                                    level=logging.INFO)
            except FileNotFoundError as e:
                os.mkdir(cwd)
                logging.basicConfig(filename=cwd + "/" + today.strftime("%d_%m_%Y_%H_%M_%S") + ".log",
                                    level=logging.INFO)

            LOG_FILENAME = filaname + '.csv'
            logging.basicConfig(format=format, filename=LOG_FILENAME, level=logging.INFO)
            logging.debug('This message should go to the log file')
        else:
            raise NotImplemented("Logger::no such logging_target" + logging_target)

    def log_info(self, msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    def log_warn(self, msg, *args, **kwargs):
        logging.warning(msg, *args, **kwargs)
