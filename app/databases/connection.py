from typing import Type
from app.databases.config import Config
from asyncpg import Connection
from uuid import uuid4
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# fix asyncpg.exceptions.InvalidSQLStatementNameError: prepared statement "
# __asyncpg_stmt_4c" does not exist
# discussion:
# https://github.com/sqlalchemy/sqlalchemy/issues/6467#issuecomment-1187494311


Session = async_sessionmaker(expire_on_commit=False)


class SQLAlchemyConnection(Connection):
    """
    class required for fixing bug mentioned above
    """

    def _get_unique_id(self, prefix: str) -> str:
        return f'__asyncpg_{prefix}_{uuid4()}__'


def engine_factory(db_url: Type[Config]):
    c = db_url()
    return create_async_engine(
        url=c.db_dsn(),
        echo=True,
        connect_args={
            'statement_cache_size': 0,  # required by asyncpg
            'prepared_statement_cache_size': 0,  # required by asyncpg
            'connection_class': SQLAlchemyConnection,
        },
        pool_pre_ping=True,
    )


async def get_session():
    async with Session() as ses:
        yield ses

