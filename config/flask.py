import os


FLASK_DEBUG = str(os.environ.get("FLASK_DEBUG"))
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
FLASK_RUN_PORT = str(os.environ.get("FLASK_RUN_PORT"))
FLASK_RUN_HOST = str(os.environ.get("FLASK_RUN_HOST"))
