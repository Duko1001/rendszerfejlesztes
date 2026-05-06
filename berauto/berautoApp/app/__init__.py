from apiflask import APIFlask
from config import Config
from app.extensions import db
from flask_migrate import Migrate
from flask_cors import CORS


def create_app(config_class=Config):
    #app = Flask(__name__)
    app = APIFlask(__name__, json_errors=True, title="Berauto API", docs_path="/swagger")
    app.config.from_object(config_class)
    CORS(app) 

    # Initialize Flask extensions here
    db.init_app(app)

    migrate = Migrate(app, db, render_as_batch=True)

    from app import models

    from app.blueprints import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    return app