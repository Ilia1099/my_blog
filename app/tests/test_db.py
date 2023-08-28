import logging
from starlette.testclient import TestClient
from app.main import app
from app.databases.config import Config, SettingsConfigDict
from app.databases.connection import Session, engine_factory

pytest_plugins = ('pytest_asyncio',)
logging.basicConfig(level=logging.INFO)


class TestConf(Config):
    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")


eng = engine_factory(TestConf)
Session.configure(bind=eng)


test_app = TestClient(app)
# test_app = app


