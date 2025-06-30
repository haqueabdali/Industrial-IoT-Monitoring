const socketio = require('socket.io');
const mongoose = require('mongoose');
const SensorReading = require('../models/SensorReading');

module.exports = function(server) {
  const io = socketio(server, {
    cors: {
      origin: "*",
      methods: ["GET", "POST"]
    }
  });

  // MongoDB change stream
  mongoose.connection.once('open', () => {
    const changeStream = SensorReading.watch();
    
    changeStream.on('change', (change) => {
      if (change.operationType === 'insert') {
        io.emit('sensor-data', change.fullDocument);
      }
    });
  });

  io.on('connection', (socket) => {
    console.log('New client connected: ' + socket.id);
    
    // Send last 10 readings on connect
    SensorReading.find().sort({ timestamp: -1 }).limit(10)
      .then(readings => {
        socket.emit('initial-data', readings.reverse());
      });
  });
};
