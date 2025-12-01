import express from 'express';
import dotenv from 'dotenv';

dotenv.config();

const PORT = process.env.PORT || 3323;
const JULES_API_KEY = process.env.JULES_API_KEY;

const app = express();

app.get('/', (req, res) => {
  res.json({ 
    status: 'healthy',
    service: 'Jules MCP Server',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    apiKeyConfigured: !!JULES_API_KEY,
    timestamp: new Date().toISOString() 
  });
});

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`Jules MCP Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`Jules API Key configured: ${JULES_API_KEY ? 'Yes' : 'No'}`);
});

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down');
  server.close(() => process.exit(0));
});
