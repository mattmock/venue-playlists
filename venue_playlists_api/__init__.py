"""API package initialization."""
import os
import logging
from flask import Flask
from flask_cors import CORS
from .config import get_config

def create_app(test_config=None):
    """Create and configure the Flask application.
    
    Args:
        test_config: Configuration dictionary to override defaults
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load config based on environment
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Override with test config if provided
    if test_config:
        app.config.update(test_config)
    
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format=app.config['LOG_FORMAT']
    )
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS']
        }
    })
    
    # Register blueprints
    from venue_playlists_api import venues
    app.register_blueprint(venues.bp)
    
    # Log startup configuration in debug mode
    if app.debug:
        app.logger.debug(f"Starting application with config: {config_class.__name__}")
        app.logger.debug(f"VENUE_DATA_DIR: {app.config['VENUE_DATA_DIR']}")
        app.logger.debug(f"CORS origins: {app.config['CORS_ORIGINS']}")
    
    return app

# Create the application instance
app = create_app() 