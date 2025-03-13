import os
import shutil

from ..task import Task


class MergeDirectoriesTask(Task):
    def execute(self):
        nr_steps = 0
        for input_files in self.inputs().values():
            nr_steps += len(input_files)
        step = 0
        keep_duplicates = self.param('keep_duplicates', False)
        for input_files in self.inputs().values():
            for source in input_files:
                source_name = os.path.split(source)[1]
                target = os.path.join(self.output('output'), source_name)
                if keep_duplicates and os.path.exists(target):
                    items = os.path.splitext(target)
                    target = items[0] + '-1' + items[1]
                shutil.copy(source, target)
                self.set_progress(step, nr_steps)
                step += 1