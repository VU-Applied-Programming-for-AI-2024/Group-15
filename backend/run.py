import logging
from app import create_app
from waitress import serve

logging.basicConfig(level=logging.DEBUG)

app = create_app()

if __name__ == '__main__':
    print("Starting server...")
    serve(app, host='0.0.0.0', port=8000)

    print("Server started successfully.")