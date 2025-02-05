from sqlalchemy.dialects import registry

print("All available dialects:")
for dialect in registry.impls:
    print(f"- {dialect}")

print("\nTrying to load PostgreSQL driver directly:")
try:
    import psycopg2
    print("psycopg2 loaded successfully!")
except ImportError:
    print("psycopg2 not found") 