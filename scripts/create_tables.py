from app.db.base import Base
from app.db.session import engine

# Important: load all models before creating tables
import app.db.models

def create_tables():
    Base.metadata.create_all(bind=engine)

    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()