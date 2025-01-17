from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # For local development
    
    # Register blueprints
    from . import venues
    app.register_blueprint(venues.bp)
    
    return app
