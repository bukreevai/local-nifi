from typing import (
    Literal,
    List
)
from os import (
    path,
    listdir,
    remove,
    mkdir
)
import shutil

from .config import Conf
from .utils import Zipper
import logging

logger = logging.getLogger(__name__)

class Driver:
    def __init__(
        self,
        config: Conf
    ):
        self.config = config
        self.host = 'localhost'
        self.container_up_command = ["docker-compose", "up", "-d"]
        self.user_guid = 1000
        self.user_group_guid = 1000

    
    def drive(self, directon: Literal['up', 'down']):
        if directon == 'up':
            self._up_driving()
        elif directon == 'down':
            self._down_driving()
        else:
            raise ValueError(f'Not correctly direction of service driving. Possible values is - "up" or "down". Currently is {directon}', )
        
    def _up_driving(self):
        self._print_separator('Prepare for deployment')
        self._db_init()
        self._nifi_init()


    def _db_init(self) -> None:
        # todo: change to iterrator
        self._print_separator('DB Init')
        service_dirs = self._make_service_dirs(self.config.db, self.config.db_dirs)
        self._make_pathes_dirs(service_dirs)
        logger.info(f'DB directories was prepared')
        for script_file in [path.join(self.config.init_db, script) for script in self.config.init_db_scripts]:
            Zipper.unzip(
                script_file,
                path.join(self.config.db, 'init')
            )
            logger.info(f'Script file {script_file} was extracted')
        self._print_separator('DB Init complete')

    def _nifi_init(self) -> None:
        self._print_separator('NIFI Setup')
        service_dirs = self._make_service_dirs(self.config.nifi, self.config.nifi_dirs)
        self._make_pathes_dirs(service_dirs)
        logger.info('NIFI directories was prepared')
        NIFI_TARGET_PATH = [self.config.init_nifi, 'conf', 'nifi_conf.tar.gz']
        logger.debug(f'NIFI TARGET CONF\t{NIFI_TARGET_PATH}')
        NIFI_SOURCE_PATH_CONF = [self.config.nifi, 'conf']
        logger.debug(f'NIFI SOURCE CONF\t{NIFI_SOURCE_PATH_CONF}')
        nifi_conf_tar = self._make_path(NIFI_TARGET_PATH)
        nifi_target_conf_path = self._make_path(NIFI_SOURCE_PATH_CONF)
        Zipper.extract_from_tar(nifi_conf_tar, nifi_target_conf_path)
        logger.info(f'NIFI config was prepared')
        self._print_separator('NIFI Setup completed')

    def _print_separator(self, separator_text) -> None:
        logger.info(f'#############\t {separator_text} \t##########')

    def _run_subrocess(self, command: List[str]):
        import subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            raise Exception(f'Error - {stderr.decode()}')

    def _down_driving(self):
        self._clear_folder(self.config.nifi)
        logger.info('NIFI folder was cleaned')
        self._clear_folder(self.config.db)
        logger.info('DB folder was cleaned') 

    def _clear_folder(self, directory) -> None:
        """
        Deletes all files and subdirectories in the specified directory.

        :param directory: Path to the directory whose contents are to be deleted.
        """
        # Check if the directory exists
        if not path.exists(directory):
            logger.warn(f"Directory '{directory}' does not exist.")
            return

        # Check if the path is indeed a directory
        if not path.isdir(directory):
            logger.warn(f"'{directory}' is not a directory.")
            return

        # Iterate over and delete each item in the directory
        for filename in listdir(directory):
            file_path = path.join(directory, filename)
            if path.isfile(file_path) or path.islink(file_path):
                try:
                    remove(file_path)
                    logger.debug(f"{file_path} was deleted")
                except Exception as error:
                    logger.error(f"Can't remove file {file_path} - {str(error)}")
            elif path.isdir(file_path):
                try: 
                    shutil.rmtree(file_path)
                    logger.debug(f"{file_path} was deleted")
                except shutil.Error as error:
                    logger.error(f"Can't remove directory {file_path} - {str(error)}")
            else:
                logger.warn(f"Skipping unknown item: '{filename}'")

    def _make_path(self, pathes: List[str]) -> str:
        return path.join(*pathes)
    
    def _make_service_dirs(self, service_root_dir: str, service_sub_dirs: List[str]) -> List[str]:
        return [path.join(service_root_dir, sub_dir) for sub_dir in service_sub_dirs]
    
    def _make_pathes_dirs(self, pathes: List[str]) -> None:
        for dir_path in pathes:
            self._make_dir(dir_path)
    
    def _make_dir(self, dir_path) -> None:
        if not path.exists(dir_path):
            mkdir(dir_path)
            logger.debug(f'{dir_path} was created')
        else:
            logger.warn(f'{dir_path} exists')
        