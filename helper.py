import datetime
import shutil

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union
def read_file(file_name):
    #f = open(file_name)
    with open(file_name) as f:
        res = f.read()
    return res


class FileReader:
    def __init__(self,path: Union[str,Path]):
        self.path : Path = Path(path).absolute()

        self.path.mkdir(parents=True,exist_ok=True)
    def read_file(self,file_name : str):
        full_path = self.path / file_name

        if not full_path.is_file():
            raise KeyError("File {file_name} cannot be found!")
        with full_path.open("r",encoding = 'utf-8') as f:
            return f.read()