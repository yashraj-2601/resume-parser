# app/wsgi.py
from flask import Flask, redirect
from flasgger import Swagger
from .routes import api_bp
from .config import settings
from .database import init_db

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SWAGGER"] = {"title": "Automated Resume Parser API", "uiversion": 3}
    Swagger(app)

    # DB
    init_db(settings.DATABASE_URL)

    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    # Health
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # Redirects to Swagger UI
    @app.get("/")
    def index():
        return redirect("/apidocs", code=302)

    @app.get("/docs")
    def docs_redirect():
        return redirect("/apidocs", code=302)

    return app

# Gunicorn entrypoint: module:variable
app = create_app()
