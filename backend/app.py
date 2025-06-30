from flask import Flask, request, jsonify
from database import save_sensor_data
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        # Save to MongoDB
        save_sensor_data(data)
        return jsonify({"status": "success", "message": "Data stored"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "iot-backend"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
