from flask import request, jsonify
from app import db
from . import sensor_bp
from datetime import datetime
from app.models.sensor import SensorReading

@sensor_bp.route('/sensors', methods=['POST'])
def receive_sensor_data():
    data = request.json
    
    # Validate required fields
    required = ['device_id', 'temperature', 'humidity']
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create new reading
    new_reading = SensorReading(
        device_id=data['device_id'],
        timestamp=datetime.utcnow(),
        temperature=float(data['temperature']),
        humidity=float(data['humidity']),
        vibration=float(data.get('vibration', 0.0))
    
    # Save to database
    db.session.add(new_reading)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Data stored",
        "id": str(new_reading.id)
    }), 201
