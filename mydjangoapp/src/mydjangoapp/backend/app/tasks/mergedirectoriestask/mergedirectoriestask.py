import os
import shutil

from ..task import Task


class MergeDirectoriesTask(Task):
    def execute(self):
        return {}