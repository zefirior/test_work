import pathlib
from environs import Env


class Environ(Env):
    DEFAULT_DB = 'postgresql://postgres@localhost:6000/postgres'
    DEFAULT_URL = '127.0.0.1:5000'

    @property
    def db_url(self):
        return self('APP_DB_URL', self.DEFAULT_DB)

    @property
    def server_name(self):
        return self("APP_SERVERNAME", self.DEFAULT_URL)

    @property
    def log_level(self):
        return self('APP_LOG_LEVEL', 'INFO')

    @property
    def root_path(self):
        return pathlib.Path(__file__).parent.parent

    @property
    def env_path(self):
        return pathlib.Path(__file__).parent


env = Environ()

env.read_env(env.env_path)
