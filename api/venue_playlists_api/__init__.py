"""API package initialization."""
from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    
    # Configure CORS for development
    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:8000",
                "http://127.0.0.1:8000",
                "http://[::]:8000"
            ]
        }
    })
    
    # Register blueprints
    from . import venues
    app.register_blueprint(venues.bp)
    
    return app

# Create the application instance
app = create_app()
