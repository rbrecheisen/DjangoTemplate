import os
import shutil

from ..task import Task


class MergeDirectoriesTask(Task):
    def execute(self):
        for f in self.input_files('input1'):
            source = f
            target = os.path.join(self.output_dir('output1'), source)
            shutil.copy(source, target)