import os
from app import app

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV') or 'development'
    app.config.from_object(f'config.{env.capitalize()}Config')
    app.run()
