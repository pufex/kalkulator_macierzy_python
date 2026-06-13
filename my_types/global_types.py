from typing import TypedDict
from numpy import ndarray
from file_management.files import FileManager

class CtxDict(TypedDict):
    f_manager: FileManager
    matrices: list[ndarray]