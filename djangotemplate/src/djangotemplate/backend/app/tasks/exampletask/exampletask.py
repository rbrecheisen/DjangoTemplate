import time

from ..task import Task
from ...managers.logmanager import LogManager

LOG = LogManager()


class ExampleTask(Task):
    def execute(self):
        for i in range(self.param('nr_iters')):
            delay = self.param('delay')
            LOG.info(f'Waiting {delay} seconds...')
            time.sleep(delay)
        return {'output1': []}