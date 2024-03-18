
from flask import Flask
from config.database import db
from routes.index import index_bp
from routes.entries import entries_bp
from config.database import db, configure_local_database
from config.assets_registering import register_assets_for
from config.flask import FLASK_RUN_PORT, FLASK_RUN_HOST, FLASK_DEBUG, FLASK_SECRET_KEY

# Setting up the app
app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
configure_local_database(app)
register_assets_for(app)
db.init_app(app)

# Registering routes
app.register_blueprint(index_bp)
app.register_blueprint(entries_bp)


# Starts the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, debug=FLASK_DEBUG)
