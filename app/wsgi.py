import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
from .config import get_settings
from .database import init_db
from .routes import api_bp
from flask import redirect

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    settings = get_settings()
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL

    Swagger(app, template={"info": {"title": "Automated Resume Parser API", "version": "1.0.0"}})
    init_db(settings.DATABASE_URL)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.get("/")
def index():
    return redirect("/apidocs", code=302)

@app.get("/docs")
def docs_redirect():
    return redirect("/apidocs", code=302)

    return app

app = create_app()

