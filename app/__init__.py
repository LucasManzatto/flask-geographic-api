from flask import Flask


def create_app() -> Flask:
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.

    Example:
        app = create_app()
        app.run(host='0.0.0.0', port=5000)
    """
    app = Flask(__name__)

    from app.controllers import trips_controller

    app.register_blueprint(trips_controller.trips_blueprint)
    return app
