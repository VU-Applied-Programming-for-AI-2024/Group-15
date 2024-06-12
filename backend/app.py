from app import create_app
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = create_app()
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

if __name__ == "__main__":
    app.run(debug=True)