import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hw_29.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
