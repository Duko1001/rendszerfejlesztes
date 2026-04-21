from apiflask import APIFlask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    #app = Flask(__name__)
    app = APIFlask(__name__, json_errors=True, title="Berauto API", docs_path="/swagger")
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from app import models

    from app.blueprints import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    return app