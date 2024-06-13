from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

data = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/api/items', methods=['POST'])
def add_item():
    new_item = request.json
    data.append(new_item)
    return jsonify(new_item), 201

@app.route('/')
def manual_schedule():

    return render_template('manual_schedule.html')

if __name__ == "__main__":
    app.run(debug=True)

