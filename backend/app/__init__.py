from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Import the blueprint
    from .routes import main

    # Register the blueprint
    app.register_blueprint(main)

    return app
