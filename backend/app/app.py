from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/calories_burned', methods=['GET'])
def calories_burned():
    exercises = [
        {"name": "Push-up", "calories": 100},
        {"name": "Sit-up", "calories": 50},
        # Add more exercises here
    ]
    return jsonify({"exercises": exercises})

if __name__ == '__main__':
    app.run(debug=True)
