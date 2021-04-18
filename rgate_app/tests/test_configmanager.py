import os
import yaml
from unittest import TestCase

from rgate_app.configmanager import YMLconfigReader


class YMLconfigReaderTest(TestCase):
    def test_validate(self):
        config_file_path = 'abc.txt'

        with self.subTest('When file does not exists'):
            with self.assertRaises(Exception):
                YMLconfigReader(config_file_path).validate()

        with self.subTest('When file exists'):
            file_name = 'test.yml'
            open(file_name, 'w')
            config_file_path = f'{os.getcwd()}/{file_name}'
            self.assertIsNone(YMLconfigReader(config_file_path).validate())
            os.remove(config_file_path)

    def test_read(self):
        with self.subTest('When test file have no data'):
            file_name = 'test.yml'
            test_config_file = open(file_name, 'w')
            config_file_path = f'{os.getcwd()}/{file_name}'
            self.assertIsNone(YMLconfigReader(config_file_path).read())

        with self.subTest('When test file have data'):
            config_data = {'A':'a', 'B':{'C':'c', 'D':'d', 'E':'e'}}
            yaml.dump(config_data, test_config_file, default_flow_style=False)
            self.assertEqual(
                YMLconfigReader(config_file_path).read(),
                config_data
            )
            os.remove(config_file_path)
