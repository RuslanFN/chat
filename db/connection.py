from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from os import getenv
from dotenv import load_dotenv
load_dotenv()
host = getenv('DB_HOST')
port = getenv('DB_PORT')
name = getenv('DB_NAME')
user = getenv('DB_USER')
password = getenv('DB_PASSWORD')
connection_string = f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}'
engine = create_async_engine(connection_string, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
