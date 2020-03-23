import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, logging_target: str):
        self.logger = logging.getLogger('DrivingScorer')
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d,%(message)s', datefmt='%Y-%m-%d,%H:%M:%S')

        if logging_target == "CONSOLE":

            ch = logging.StreamHandler()  # Create console handler with a higher log level
            ch.setLevel(logging.INFO)

            ch.setFormatter(formatter)  # Create formatter and add it to the handlers

            self.logger.addHandler(ch)  # Add the handlers to logger

        elif logging_target == "CSV":

            today = datetime.now()
            cwd = os.getcwd()
            cwd = os.path.split(cwd)[0] + "/Data/"
            filename = cwd + "/" + today.strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
            print("Record file: %s" % filename)

            fh = logging.FileHandler(filename)  # Create file handler which logs even debug messages
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        else:
            raise NotImplemented("Logger::no such logging_target %s", logging_target)

    def log_info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def log_warn(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
