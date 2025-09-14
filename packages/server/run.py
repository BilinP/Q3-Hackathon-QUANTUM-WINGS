#!/usr/bin/env python3
"""
Production runner for the Quantum TSP Solver API
"""

import os
import logging
from app import app
from config import config

def create_app():
    """Create and configure the Flask app"""
    
    # Get configuration
    config_name = os.environ.get('FLASK_ENV', 'development')
    app_config = config.get(config_name, config['default'])
    
    # Configure logging
    log_level = getattr(logging, app_config.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting Quantum TSP Solver API in {config_name} mode")
    logger.info(f"Configuration: {app_config.__name__}")
    
    return app, app_config

if __name__ == '__main__':
    app, config_obj = create_app()
    
    app.run(
        host='0.0.0.0',
        port=config_obj.PORT,
        debug=config_obj.DEBUG
    )
