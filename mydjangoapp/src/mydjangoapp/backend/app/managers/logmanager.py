import logging

from ..models import LogOutputModel

LOG = logging.getLogger('mydjangoapp')


class LogManager:
    def __init__(self):
        pass

    def write_to_db(self, message, mode):
        LogOutputModel.objects.create(_message=message, _mode=mode)

    def info(self, message):
        LOG.info(message)
        self.write_to_db(message, 'info')

    def warning(self, message):
        LOG.warning(message)
        self.write_to_db(message, 'warning')

    def error(self, message):
        LOG.error(message)
        self.write_to_db(message, 'error')

    def get_messages(self):
        return LogOutputModel.objects.all()
    
    def delete_messages(self):
        for model in LogOutputModel.objects.all():
            model.delete()