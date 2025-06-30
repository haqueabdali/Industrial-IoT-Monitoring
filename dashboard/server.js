const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mongoose = require('mongoose');
const Data = require('./models/SensorData');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: '*' } });

// MongoDB Connection
mongoose.connect('mongodb://mongodb:27017/iot_factory', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// Socket.IO for real-time updates
io.on('connection', (socket) => {
  console.log('Dashboard client connected');
  
  // Watch MongoDB change stream
  const changeStream = Data.watch();
  changeStream.on('change', (change) => {
    if (change.operationType === 'insert') {
      socket.emit('new-data', change.fullDocument);
    }
  });
  
  // Get historical data
  Data.find().sort({ timestamp: -1 }).limit(20)
    .then(data => socket.emit('historical-data', data.reverse()));
});

// Serve static files
app.use(express.static('public'));

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Dashboard running on port ${PORT}`);
});
