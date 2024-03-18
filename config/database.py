import os
from pathlib import Path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()


def configure_local_database(app):
    db_path = os.getenv('LOCAL_DATABASE_PATH')
    if not db_path:
        raise RuntimeError("LOCAL_DATABASE_PATH is not set")
    os.makedirs(db_path, exist_ok=True)

    project_dir = Path(__file__).resolve().parent.parent
    db_uri = f'sqlite:///{project_dir}/{db_path}/results.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri