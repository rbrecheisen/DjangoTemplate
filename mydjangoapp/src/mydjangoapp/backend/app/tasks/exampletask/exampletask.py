import time

from ..task import Task


class ExampleTask(Task):
    def execute(self):
        for i in range(self.param('nr_iters')):
            delay = self.param('delay')
            time.sleep(delay)
            self.set_progress(i, self.param('nr_iters'))
