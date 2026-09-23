"""Point d'entrée Flask : crée l'application et enregistre les blueprints."""
from flask import Flask
from flask_cors import CORS

from config import config
from src.presentation.routes.alert_routes import alert_bp
from src.presentation.routes.auth_routes import auth_bp
from src.presentation.routes.blockchain_routes import blockchain_bp
from src.presentation.routes.certificate_routes import certificate_bp
from src.presentation.routes.health_routes import health_bp
from src.presentation.routes.inspection_routes import inspection_bp
from src.presentation.routes.lot_routes import lot_bp
from src.presentation.routes.measurement_routes import measurement_bp
from src.presentation.routes.qr_routes import qr_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = config.max_upload_mb * 1024 * 1024
    CORS(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(lot_bp)
    app.register_blueprint(measurement_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(inspection_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(blockchain_bp)
    app.register_blueprint(certificate_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=config.flask_host, port=config.flask_port, debug=config.debug)
