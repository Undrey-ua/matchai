from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# URL вашої бази даних
DATABASE_URL = "postgresql+psycopg2://andrii@localhost:5432/fastapi_db"

try:
    # Створюємо engine
    engine = create_engine(DATABASE_URL, echo=True)
    
    # Пробуємо підключитися
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        
except SQLAlchemyError as e:
    print(f"Database connection error: {str(e)}") 