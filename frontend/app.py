from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Config:
    DEBUG = True
    BACKEND_ENDPOINT = 'http://localhost:5000'

app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manual_schedule')
def manual_schedule():
    return render_template('manual_schedule.html')

@app.route('/AIschedule')
def ai_schedule():
    return render_template('AIschedule.component.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=5001)
