from sqlalchemy import create_engine, text

# Спробуємо підключитися
engine = create_engine('postgresql+psycopg2://andrii@localhost:5432/fastapi_db')

try:
    # Перевіряємо з'єднання
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("З'єднання успішне!")
except Exception as e:
    print(f"Помилка: {str(e)}") 