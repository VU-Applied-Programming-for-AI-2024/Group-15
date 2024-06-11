import logging
from app import create_app
from waitress import serve

logging.basicConfig(level=logging.DEBUG)

app = create_app()

if __name__ == '__main__':
    print("Starting server...")
    print("Server started successfully.")