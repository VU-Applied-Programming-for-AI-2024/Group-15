from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


@app.route('/')
def create_app():
    app = Flask(__name__)

    from app.routes import register_routes
    register_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)



