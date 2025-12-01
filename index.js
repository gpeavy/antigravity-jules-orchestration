import express from 'express';
import dotenv from 'dotenv';
import https from 'https';

dotenv.config();

const PORT = process.env.PORT || 3323;
const JULES_API_KEY = process.env.JULES_API_KEY;

const app = express();
app.use(express.json());

// Root endpoint - service metadata
app.get('/', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Jules MCP Server',
    version: '1.3.0',
    timestamp: new Date().toISOString(),
    capabilities: ['sessions', 'tasks', 'orchestration', 'mcp-protocol', 'sources'],
    authMethod: 'api-key'
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    apiKeyConfigured: !!JULES_API_KEY,
    timestamp: new Date().toISOString()
  });
});

// Extended health check
app.get('/api/v1/health', (req, res) => {
  res.json({
    status: 'ok',
    version: '1.3.0',
    services: {
      julesApi: JULES_API_KEY ? 'configured' : 'not configured',
      database: 'not required'
    },
    timestamp: new Date().toISOString()
  });
});

// MCP Protocol - List available tools
app.get('/mcp/tools', (req, res) => {
  res.json({
    tools: [
      {
        name: 'jules_list_sources',
        description: 'List all connected GitHub repositories (sources)',
        parameters: {}
      },
      {
        name: 'jules_create_session',
        description: 'Create a new Jules coding session for autonomous development',
        parameters: {
          source: { type: 'string', required: true, description: 'Source name (e.g., sources/github/owner/repo)' },
          task: { type: 'string', required: true, description: 'Task description for Jules' }
        }
      },
      {
        name: 'jules_list_sessions',
        description: 'List all Jules sessions',
        parameters: {}
      },
      {
        name: 'jules_get_session',
        description: 'Get details of a specific session',
        parameters: {
          sessionId: { type: 'string', required: true, description: 'Session ID to retrieve' }
        }
      },
      {
        name: 'jules_send_message',
        description: 'Send a message to an existing Jules session',
        parameters: {
          sessionId: { type: 'string', required: true, description: 'Session ID' },
          message: { type: 'string', required: true, description: 'Message to send' }
        }
      }
    ]
  });
});

// MCP Protocol - Execute tool
app.post('/mcp/execute', async (req, res) => {
  const { tool, parameters } = req.body;

  if (!tool) {
    return res.status(400).json({ error: 'Tool name required' });
  }

  if (!JULES_API_KEY) {
    return res.status(500).json({ error: 'JULES_API_KEY not configured' });
  }

  try {
    let result;
    switch (tool) {
      case 'jules_list_sources':
        result = await listSources();
        break;
      case 'jules_create_session':
        result = await createJulesSession(parameters);
        break;
      case 'jules_list_sessions':
        result = await listJulesSessions();
        break;
      case 'jules_get_session':
        result = await getJulesSession(parameters.sessionId);
        break;
      case 'jules_send_message':
        result = await sendMessage(parameters.sessionId, parameters.message);
        break;
      default:
        return res.status(400).json({ error: 'Unknown tool: ' + tool });
    }
    res.json({ success: true, result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Jules API helper - make authenticated request
function julesRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'jules.googleapis.com',
      port: 443,
      path: '/v1alpha' + path,
      method: method,
      headers: {
        'X-Goog-Api-Key': JULES_API_KEY,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (response) => {
      let data = '';
      response.on('data', chunk => data += chunk);
      response.on('end', () => {
        if (response.statusCode >= 200 && response.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(data);
          }
        } else {
          reject(new Error('Jules API error: ' + response.statusCode + ' - ' + data));
        }
      });
    });

    req.on('error', reject);
    
    if (body) {
      const jsonBody = JSON.stringify(body);
      req.setHeader('Content-Length', Buffer.byteLength(jsonBody));
      req.write(jsonBody);
    }
    req.end();
  });
}

// List all connected sources (repositories)
async function listSources() {
  return await julesRequest('GET', '/sources');
}

// Create a new Jules session
async function createJulesSession(config) {
  const sessionData = {
    source: config.source,
    task: config.task
  };
  return await julesRequest('POST', '/sessions', sessionData);
}

// List all sessions
async function listJulesSessions() {
  return await julesRequest('GET', '/sessions');
}

// Get session details
async function getJulesSession(sessionId) {
  return await julesRequest('GET', '/sessions/' + sessionId);
}

// Send message to session
async function sendMessage(sessionId, message) {
  return await julesRequest('POST', '/sessions/' + sessionId + ':sendMessage', { message });
}

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log('Jules MCP Server running on port ' + PORT);
  console.log('Health check: http://localhost:' + PORT + '/health');
  console.log('MCP Tools: http://localhost:' + PORT + '/mcp/tools');
  console.log('Jules API Key configured: ' + (JULES_API_KEY ? 'Yes' : 'No'));
});

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down');
  server.close(() => process.exit(0));
});
