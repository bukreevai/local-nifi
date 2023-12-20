from dataclasses import (
    dataclass,
    field
)
from typing import List
from os import (
    path,
    getcwd,
    listdir,
    sep
)

@dataclass
class Conf:
    hosts_file: str = None
    project:str = getcwd()
    init_dir: str = path.join(project, 'init')
    init_db:str = path.join(init_dir, 'db')
    init_nifi:str = path.join(init_dir, 'nifi')
    nifi:str = path.join(project, 'nifi')
    db:str = path.join(project, 'postgres')
    scripts:str = path.join(project, 'scripts')
    env_hosts: str = path.join(scripts, 'hosts_list.txt')
    init_db_scripts: List[str] = field(default_factory=list, init=True)

    def __post_init__(self):
        self.init_db_scripts = listdir(self.init_db)




windows_config = Conf(
    hosts_file = path.join('C:', sep, 'Windows', 'System32', 'drivers', 'etc', 'hosts'),
)

unix_config = Conf(
    hosts_file = path.join('/', 'etc', 'hosts'),
)
