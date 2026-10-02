/* PassManager — Node.js frontend server */
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const os = require('os');

const app = express();
const PORT = process.env.PORT || 4747;
const FLASK_URL = process.env.FLASK_URL || 'http://127.0.0.1:5000';

// Proxy all /api/* requests to Flask backend
app.use('/api', createProxyMiddleware({
  target: FLASK_URL,
  changeOrigin: true,
  onError: (err, req, res) => {
    res.status(502).json({ error: 'Backend offline. Is app.py running?' });
  }
}));

// Serve static files (index.html)
app.use(express.static(__dirname, { index: 'index.html' }));

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));

app.listen(PORT, '0.0.0.0', () => {
  // Apna local IP nikaalo
  const nets = os.networkInterfaces();
  let localIP = 'localhost';
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        localIP = net.address;
        break;
      }
    }
    if (localIP !== 'localhost') break;
  }

  console.log('='.repeat(62));
  console.log('  PassManager — Frontend');
  console.log(`  → Local:   http://localhost:${PORT}`);
  console.log(`  → Network: http://${localIP}:${PORT}`);
  console.log(`  → Proxying /api → ${FLASK_URL}`);
  console.log('='.repeat(62));
});