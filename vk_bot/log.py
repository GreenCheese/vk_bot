import logging


class Log:
    @staticmethod
    def get_logger(log_file):
        logger = logging.getLogger('vk_bot_application')
        logger.propagate = False  # disable console output

        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger
