from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        extra="ignore"
    )

    PROJECT_NAME: str
    VERSION: str
    ENVIRONMENT: str
    URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXP_MIN: int

    DB_SCHEME: str
    DB_HOSTNAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    MAX_FILE_SIZE_MB: int
    UPLOAD_PATH: str

    EXP_TIME_VOUCHER_MIN: int

    @computed_field()
    @property
    def DB_PATH(self) -> str:
        sub = "dev" if self.ENVIRONMENT == "development" else "prod"
        return f"{self.DB_NAME}-{sub}"

    @computed_field()
    @property
    def DB_URL(self) -> str:
        url =  MultiHostUrl.build(
            scheme=self.DB_SCHEME,
            host=self.DB_HOSTNAME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            path=self.DB_PATH
        )

        return str(url)


settings = Settings() # type: ignore
