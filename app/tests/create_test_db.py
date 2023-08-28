from app.databases.connection import engine_factory, Session, get_session
from app.databases.config import Config, SettingsConfigDict
import app.models as mod
import asyncio


class TestConf(Config):
    model_config = SettingsConfigDict(env_file=".env.test", extra="ignore")


eng = engine_factory(TestConf)
Session.configure(bind=eng)


async def drop_create():
    async with eng.begin() as conn:
        await conn.run_sync(mod.Base.metadata.drop_all)
        await conn.run_sync(mod.Base.metadata.create_all)
    await eng.dispose()


if __name__ == "__main__":
    asyncio.run(drop_create())
