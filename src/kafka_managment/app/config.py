from pydantic_settings import BaseSettings


class Config(BaseSettings):
    debug: bool = False
    postgres_host: str = "postgres.local"
    postgres_port: int = 5432
    postgres_username: str = "postgres"
    postgres_password: str = "postgres"
    postgres_database: str = "demo"

    @property
    def postgres_conecction_string(self) -> str:
        """
        Make connection string for SQLAlchemy
        """
        return f'postgresql+psycopg2://{self.postgres_username}:\
            {self.postgres_password}@{self.postgres_host}:\
                {self.postgres_port}/{self.postgres_database}'


config = Config()
