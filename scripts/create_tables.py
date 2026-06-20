from app.db.base import Base
from app.db.session import engine

# Important: load all models
import app.db.models

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")