from sqlalchemy import create_engine
from app.core.config import settings 

engine = create_engine(
    settings.DATABASE_URL,
    echo=False, #for session 
    #One database connection has been idle for 20 minutes.Database closes it.
    pool_pre_ping=True
)