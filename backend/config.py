import os

# Database URL (use SQLite for now)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crime_system.db")
