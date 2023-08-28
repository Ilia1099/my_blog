from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal
from pydantic import SecretStr, PostgresDsn, Field


class Config(BaseSettings):
    db_protocol: str
    db_host: str
    db_user: str
    db_password: SecretStr
    db_port: str
    db_name: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def db_dsn(self, protocol: str = None):
        protocol = protocol or self.db_protocol
        url = f"{protocol}://"
        if self.db_user:
            url += self.db_user
        if self.db_password:
            url += ':' + self.db_password.get_secret_value()
        if self.db_user or self.db_password:
            url += '@'
        url += self.db_host
        if self.db_port:
            url += ':' + self.db_port
        if self.db_name:
            url += f"/{self.db_name}"
        return url
