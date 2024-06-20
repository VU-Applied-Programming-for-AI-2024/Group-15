def create_app():
    from flask import Flask
    app = Flask(__name__)
    from .routes import register_routes
   