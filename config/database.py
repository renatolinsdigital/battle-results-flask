import os
from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db: SQLAlchemy = SQLAlchemy()


def configure_local_database(app: Flask):
    db_path: str | None = os.getenv('LOCAL_DATABASE_PATH')

    if db_path is None:
        raise RuntimeError("LOCAL_DATABASE_PATH is not set")

    # Convert to Path object and resolve to absolute path
    db_path = Path(db_path).resolve()
    # Create directory if it doesn't exist
    db_path.mkdir(parents=True, exist_ok=True)

    db_uri: str = f'sqlite:///{db_path}/results.db'  # Create database URI
    # Configure SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
