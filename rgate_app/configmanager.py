import os
from abc import ABC, abstractmethod
from typing import NoReturn

import yaml


class ConfigReader(ABC):
    def __init__(self, config_file_path: str) -> NoReturn:
        self.config_file = config_file_path

    def validate(self) -> NoReturn:
        """This method validate given config file exists or not."""
        if not os.path.isfile(self.config_file):
            raise Exception(f'Sorry, config file {self.config_file} not exists')

    @abstractmethod
    def read(self):
        pass


class YMLconfigReader(ConfigReader):
    def __init__(self, config_file_path) -> NoReturn:
        super().__init__(config_file_path)
        self.validate()

    def read(self) -> dict:
        """Method used to read the config from given config file path."""
        with open(self.config_file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except Exception as e:
                print(e)
