import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, logging_target: str):
        self.logger = logging.getLogger('DrivingScorer')
        self.logger.setLevel(logging.INFO)

        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d,%(message)s', datefmt='%Y-%m-%d,%H:%M:%S')

        if logging_target == "CONSOLE":
            # logging.basicConfig(format=formatter,level=logging.INFO,
            #                     datefmt='%d_%m_%Y_%H_%M_%S')  # datefmt="%H:%M:%S"

            # create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            # create formatter and add it to the handlers
            ch.setFormatter(formatter)
            # add the handlers to logger
            self.logger.addHandler(ch)

        elif logging_target == "CSV":

            today = datetime.now()
            cwd = os.getcwd()
            cwd = os.path.split(cwd)[0] + "/Data/"
            filename = cwd + "/" + today.strftime("%d_%m_%Y_%H_%M_%S") + ".csv"

            # create file handler which logs even debug messages
            fh = logging.FileHandler(filename)
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            # try:
            #
            #     logging.basicConfig(format=formatter,filename=filename,
            #                         level=logging.INFO)
            # except FileNotFoundError as e:
            #     os.mkdir(filename)
            #     logging.basicConfig(format=formatter,filename=filename,
            #                         level=logging.INFO)

        else:
            raise NotImplemented("Logger::no such logging_target %s", logging_target)

    def log_info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def log_warn(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
