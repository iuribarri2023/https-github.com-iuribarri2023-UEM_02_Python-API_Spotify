from flask import Flask
from .config import Configuration
from .extensions import api as smorest_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    # Initialize API (Flask-Smorest)
    smorest_api.init_app(app)

    # Register blueprints
    from .api.spotify_api import blp as SpotifyBlueprint
    from .api.users import blp as UsersBlueprint

    smorest_api.register_blueprint(SpotifyBlueprint)
    smorest_api.register_blueprint(UsersBlueprint)

    @app.route("/")
    def index():
        """Simple landing page with docs and quick links."""
        return (
            "<!doctype html>"
            "<html lang='en'>"
            "<head><meta charset='utf-8'><title>API Euskera</title></head>"
            "<body style='font-family: Arial, sans-serif; max-width: 720px; margin: 40px auto;'>"
            "<h1>API de M\u00fasica en Euskera</h1>"
            "<p>Estado: <strong>OK</strong></p>"
            "<ul>"
            "<li><a href='/docs'>Swagger / OpenAPI UI</a></li>"
            "<li><a href='/openapi.json'>Descargar OpenAPI JSON</a></li>"
            "<li><a href='/health'>Healthcheck JSON</a></li>"
            "<li><a href='/v1/users'>Listado de usuarios</a> (GET)</li>"
            "</ul>"
            "<p>Consulta las rutas de Spotify en <code>/v1/search</code> y <code>/v1/tracks/&lt;id&gt;</code>.</p>"
            "</body></html>"
        )

    @app.route("/health")
    def health():
        """Lightweight healthcheck endpoint."""
        return {"status": "ok", "service": "api-euskera"}, 200

    return app
