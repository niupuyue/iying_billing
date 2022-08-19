import logging
from django.conf import settings
import os


class LoggingFormatter(logging.Formatter):

    def format(self, record):
        base_dir = str(settings.BASE_DIR)
        pathname = record.pathname
        pathname = pathname.replace(str(f'{base_dir}/'), '').replace('.py', '').replace('/', '.')
        record.pathname = pathname
        record.__dict__['django_settings_module'] = os.environ.get('DJANGO_SETTINGS_MODULE')
        return super(LoggingFormatter, self).format(record)


class IYingLogger(object):

    def __init__(self):
        self.logger = logging.getLogger('debug')
        self.stacklevel = 2

    @staticmethod
    def args_to_string(args):
        s = ' '.join([f'({arg})' for arg in args])
        return s

    def info(self, *args):
        s = self.args_to_string(args)
        self.logger.info(s, stacklevel=self.stacklevel)

    def debug(self, *args):
        s = self.args_to_string(args)
        self.logger.debug(s, stacklevel=self.stacklevel)

    def error(self, *args):
        s = self.args_to_string(args)
        self.logger.error(s, stacklevel=self.stacklevel)

    def critical(self, *args):
        s = self.args_to_string(args)
        self.logger.critical(s, stacklevel=self.stacklevel)

    def warning(self, *args):
        s = self.args_to_string(args)
        self.logger.warning(s, stacklevel=self.stacklevel)

    def exception(self, *args):
        s = self.args_to_string(args)
        self.logger.exception(s, stacklevel=self.stacklevel)


iyingLogger = IYingLogger()
