from dataclasses import dataclass
from enum import Enum
from os import path
from typing import Optional
import glob

class FileType(Enum):
    MONITOR = 'monitor'

@dataclass
class File:
    filepath: str
    name: str
    contents: Optional[str]

    def __init__(self, filepath: str, skip_load=False):
        self.filepath = filepath
        self.name = path.basename(filepath)

        if not skip_load:
            self.load()

    def load(self):
        with open(self.filepath, 'rb') as f:
            self.contents = f.read().decode('utf-8')

def file_search(directory: str, extension: str):
    abs_path = path.abspath(directory)
    regex_str = "{}/**/*.{}".format(abs_path, extension)
    
    filepaths = glob.glob(regex_str, recursive=True)

    return filepaths

def file_find(directory: str, file_name: str):
    abs_path = path.abspath(directory)
    regex_str = "{}/{}".format(abs_path, file_name)
    
    filepaths = glob.glob(regex_str, recursive=True)

    if len(filepaths) != 1:
        raise Exception("File not found: {}".format(regex_str))

    return filepaths[0]

def read_files(paths, extension):
    files = []

    for path in paths:
        filepaths = file_search(path, extension)

        for filepath in filepaths:
            file = File(filepath)
            files.append(file)

    return files

def read_project_files(project):
    files = {}
    files[FileType.MONITOR] = read_files(project.monitor_paths, 'y*ml')

    return files
