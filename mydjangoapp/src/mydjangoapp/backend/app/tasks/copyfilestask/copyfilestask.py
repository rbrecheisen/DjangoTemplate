import os
import shutil

from ..task import Task


class CopyFilesTask(Task):
    def execute(self):
        return {}