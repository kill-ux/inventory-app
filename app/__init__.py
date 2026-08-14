from flask import Flask
from .config import Config
from .models import db
import time
from sqlalchemy.exc import OperationalError

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    from .routes.movies import movies_bp
    from .routes.health import health_bp

    app.register_blueprint(movies_bp)
    app.register_blueprint(health_bp)
    db.init_app(app)

    connect_to_database_with_retry(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if hasattr(e, "code"):
            print(f"Error: {e}, Code: {e.code}")
            if hasattr(e, "description"):
                return {"error": e.description}, e.code
            return {"error": "An error occurred"}, e.code
        return {"error": "Internal Server Error", "message": str(e)}, 500

    return app

def connect_to_database_with_retry(app, retry_delay=3):
    with app.app_context():
        while True:
            try:
                print("Attempting to connect to the database...", flush=True)
                db.create_all()
                print("Database connection successful!", flush=True)
                break  # Connection succeeded, exit the retry loop$$$
            except OperationalError as e:
                print(f"Database not ready yet ({e}). Retrying in {retry_delay} seconds...", flush=True)
                time.sleep(retry_delay)
            except Exception as e:
                # Catch any other unexpected critical structural errors and log them
                print(f"Database setup notice (Unexpected error): {e}", flush=True)
                time.sleep(retry_delay)

import os

def get_env_variable(name, cast_type=str):
    """
    Retrieves an environment variable. 
    Raises a Detailed RuntimeError if the variable is missing.
    """
    
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"CRITICAL ERROR: Environment variable '{name}' is not set.")
    try:
        return cast_type(value)
    except ValueError:
        raise RuntimeError(f"CRITICAL ERROR: Variable '{name}' must be of type {cast_type.__name__}.")