from typing import (
    Literal
)
from os import (
    path,
    listdir,
    remove
)
import shutil

from .config import Conf
from .utils import Zipper
import re

class Driver:
    def __init__(
        self,
        config: Conf
    ):
        self.config = config
        self.IP_ADDRESS = '127.0.0.1'

    
    def drive(self, directon: Literal['up', 'down']):
        if directon == 'up':
            self._up_driving()
        elif directon == 'down':
            self._down_driving()
        else:
            raise ValueError(f'Not correctly direction of service driving. Possible values is - "up" or "down". Currently is {directon}', )
        
    def _up_driving(self):
        # 1 step: unzip init db scripts
        # todo: change to iterrator
        for host_file in [path.join(self.config.init_db, script) for script in self.config.init_db_scripts]:
            Zipper.unzip(
                host_file,
                path.join(self.config.db, 'init')
            )

        # 2 step: add hosts to host files
        with open(self.config.hosts_file, 'r') as host_file:
            existing_hosts = [host.strip() for host in host_file.readlines()]

        with open(self.config.hosts_file, 'w') as host_file:
            with open(self.config.env_hosts, 'r') as host_list:
                for host in host_list:
                    if host not in existing_hosts:
                        host_row = self._get_host_string(host)
                        host_file.write(host_row)

    def _down_driving(self):
        # Читаем строки, которые нужно удалить, из файла host_list.txt
        with open(self.config.env_hosts, 'r') as file:
            lines_to_remove = [self._get_host_string(line) for line in file.readlines()]

        # Читаем текущее содержимое файла host.txt
        with open(self.config.hosts_file, 'r') as file:
            host_content = file.read()

        # Удаляем все вхождения каждой строки из host_list.txt в host.txt
        for line in lines_to_remove:
            # Создаем регулярное выражение для поиска строки
            regex_pattern = re.escape(line) + r'(?:\r\n|\r|\n)?'
            host_content = re.sub(regex_pattern, '', host_content)

        # Перезаписываем файл host.txt без удаленных строк
        with open(self.config.hosts_file, 'w') as file:
            file.write(host_content)
        
        self._clear_folder(self.config.nifi)
        self._clear_folder(self.config.db)


    def _get_host_string(self, host) -> str:
        return f'{self.IP_ADDRESS}\t{host}'
    

    def _clear_folder(self, directory) -> None:
        """
        Deletes all files and subdirectories in the specified directory.

        :param directory: Path to the directory whose contents are to be deleted.
        """
        # Check if the directory exists
        if not path.exists(directory):
            print(f"Directory '{directory}' does not exist.")
            return

        # Check if the path is indeed a directory
        if not path.isdir(directory):
            print(f"'{directory}' is not a directory.")
            return

        # Iterate over and delete each item in the directory
        for filename in listdir(directory):
            file_path = path.join(directory, filename)
            if path.isfile(file_path) or path.islink(file_path):
                remove(file_path)
            elif path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                print(f"Skipping unknown item: '{filename}'")
        