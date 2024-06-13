from flask import Flask

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    return app

create_app()

