# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the async session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get the async session
async def get_db():
    async with async_session() as session:
        yield session