import os
import shutil

from ..task import Task


class CopyFilesTask(Task):
    def execute(self):
        input_files = self.input('input')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            source = input_files[step]
            source_name = os.path.split(source)[1]
            target = os.path.join(self.output('output'), source_name)
            shutil.copy(source, target)
            self.set_progress(step, nr_steps)