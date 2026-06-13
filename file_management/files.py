import os
import re
import numpy as np
from enum import StrEnum

def check_path_out(path):
    if path is None:
        return os.getcwd()
    elif not os.path.exists(path):
        raise ValueError
    else:
        return path

class FileManager:

    @staticmethod
    def valid_index(f_manager, i):
        return not (i <= 0 or i > f_manager.n)

    @staticmethod
    def file_name(f_manager, i):
        if not FileManager.valid_index(f_manager, i):
            raise IndexError
        return FileManager._file_prefix + str(i) + FileManager._ext

    @staticmethod
    def file_path(f_manager: FileManager, i: int):
        return os.path.join(f_manager.path, FileManager.file_name(f_manager, i))

    @staticmethod
    def config_file_path(f_manager: FileManager):
        return os.path.join(f_manager.path, f_manager._Config.name)

    @staticmethod
    def _check_if_its_save_file(el):
        pattern = f"^{FileManager._file_prefix}\\d+\\{FileManager._ext}$"
        return re.match(pattern, el)

    _file_prefix = "matrices_"
    _ext = ".txt"


    class _Config:
        @classmethod
        def get_default_props_map(cls) -> dict:
            return dict([
                (cls.Props.CURRENT_FILE, 0)
            ])

        name = "matrices.config"
        props_n = 1

        class Props(StrEnum):
            CURRENT_FILE = "CURRENT_FILE"

        @staticmethod
        def handle_raw_current_file(f_manager: FileManager, value):
            data = int(value)
            return data, data == 0 or FileManager.valid_index(f_manager, data)

        @staticmethod
        def handle_raw_data(f_manager, prop: str, value):
            config = FileManager._Config
            props = config.Props
            match prop:
                case props.CURRENT_FILE:
                    return config.handle_raw_current_file(f_manager, value)
            return False


        def __init__(self, f_manager: FileManager):
            self.f_manager = f_manager

            # V initializes self.props map using file config
            #   if it fails, uses default config prop
            self._props = FileManager._Config.get_default_props_map()
            try:
                self.load_config_file()
            except:
                pass

        def load_config_file(self):
            try:
                Config = FileManager._Config
                with open(FileManager.config_file_path(self.f_manager), "r") as file:
                    for line in file.readlines():
                        prop, value = line.removesuffix("\n").split("=") # if not enough items in list -> ValueError
                        data, isValid = Config.handle_raw_data(self.f_manager, prop, value)
                        if isValid:
                            self._props[prop] = data
                        else:
                            raise ValueError
            except Exception:
                self.update_config_file()

        def update_config_file(self, config: dict=None):
            with open(FileManager.config_file_path(self.f_manager), "w") as file:
                if config is None:
                    config = FileManager._Config.get_default_props_map()
                for prop, value in config.items():
                    file.write(f"{prop}={value}\n")

        def set_config(self, config: dict =None):
            if config is None:
                config = FileManager._Config.get_default_props_map()
            self._props = config

        @property
        def props(self):
            return self._props

        @property
        def current_file(self):
            return self._props[self.Props.CURRENT_FILE]

        @current_file.setter
        def current_file(self, i):
            if not FileManager.valid_index(self.f_manager, i):
                raise IndexError
            self._props[self.Props.CURRENT_FILE] = i

    def __init__(self, path=None):


        self._path = check_path_out(path)

        i = 0
        for el in os.listdir(self._path):
            if FileManager._check_if_its_save_file(el):
                i = i + 1

        self._file_n = i
        self._config = FileManager._Config(self)

    @property
    def path(self):
        return self._path

    @property
    def n(self):
        return self._file_n

    @property
    def current_file(self):
        return self._config.current_file

    def load_saved_file(self, i):
        matrices = []
        with open(FileManager.file_path(self, i), "r") as file:
            line = file.readline()
            while line != "":
                w = int(line.removesuffix("\n"))
                l = []
                for j in range(w):
                    l.append([float(j) for j in file.readline().split()])
                matrices.append(np.array(l))
                line = file.readline()
        self._config.current_file = i
        self._config.update_config_file(self._config.props)
        print(self._config.current_file)
        return matrices

    def save_to_file(self, i, matrices):
        with open(FileManager.file_path(self, i), "w") as file:
            for matrix in matrices:
                w = matrix.shape[0]
                file.write(f'{w}\n')
                for row in matrix:
                    numbers = [str(i) for i in row]
                    file.write(" ".join(numbers) + "\n")

    def switch_files(self, i, j):
        if i != j:
            temp = os.path.join(self.path, "temp.txt")
            i_path = FileManager.file_path(self, i)
            j_path = FileManager.file_path(self, j)
            os.rename(i_path, temp)
            os.rename(j_path, i_path)
            os.rename(temp, j_path)

    def append_save(self):
        open(FileManager.file_path(self, self._file_n + 1), "w").close()
        self._file_n = self._file_n + 1

    def print(self):
        for i in range(self._file_n):
            print(f"Save {i + 1}")


