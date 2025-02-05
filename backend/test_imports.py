import sys
print("Python path:", sys.path)

try:
    from sqlalchemy import create_engine
    print("SQLAlchemy imported successfully!")
except Exception as e:
    print(f"SQLAlchemy import error: {str(e)}")

try:
    import psycopg2
    print("psycopg2 imported successfully!")
except Exception as e:
    print(f"psycopg2 import error: {str(e)}")

try:
    from app.models.category import Category
    print("Category model imported successfully!")
except Exception as e:
    print(f"Category import error: {str(e)}")

try:
    from app.core.database import Base
    print("Base imported successfully!")
except Exception as e:
    print(f"Import error: {str(e)}") 