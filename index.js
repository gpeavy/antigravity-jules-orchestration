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
    version: '1.1.0',
    timestamp: new Date().toISOString(),
    capabilities: ['sessions', 'tasks', 'orchestration', 'mcp-protocol']
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

// MCP Protocol - List available tools
app.get('/mcp/tools', (req, res) => {
  res.json({
    tools: [
      {
        name: 'jules_create_session',
        description: 'Create a new Jules coding session for autonomous development',
        parameters: {
          repository: { type: 'string', required: true, description: 'GitHub repository (owner/repo)' },
          task: { type: 'string', required: true, description: 'Task description for Jules' },
          branch: { type: 'string', required: false, description: 'Target branch (default: main)' },
          autoApprove: { type: 'boolean', required: false, description: 'Auto-approve changes' }
        }
      },
      {
        name: 'jules_list_sessions',
        description: 'List all active Jules sessions',
        parameters: {}
      },
      {
        name: 'jules_get_session',
        description: 'Get details of a specific session',
        parameters: {
          sessionId: { type: 'string', required: true, description: 'Session ID to retrieve' }
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

  try {
    let result;
    switch (tool) {
      case 'jules_create_session':
        result = await createJulesSession(parameters);
        break;
      case 'jules_list_sessions':
        result = await listJulesSessions();
        break;
      case 'jules_get_session':
        result = await getJulesSession(parameters.sessionId);
        break;
      default:
        return res.status(400).json({ error: 'Unknown tool: ' + tool });
    }
    res.json({ success: true, result });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Jules API integration functions
async function createJulesSession(config) {
  const sessionData = {
    repository: config.repository,
    task: config.task || 'Autonomous development workflow',
    autoApprove: config.autoApprove || false,
    branch: config.branch || 'main'
  };

  return new Promise((resolve, reject) => {
    const data = JSON.stringify(sessionData);

    const options = {
      hostname: 'jules.googleapis.com',
      port: 443,
      path: '/v1alpha/sessions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length,
        'Authorization': 'Bearer ' + JULES_API_KEY
      }
    };

    const req = https.request(options, (response) => {
      let body = '';
      response.on('data', chunk => body += chunk);
      response.on('end', () => {
        if (response.statusCode === 200 || response.statusCode === 201) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error('Jules API error: ' + response.statusCode + ' - ' + body));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function listJulesSessions() {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'jules.googleapis.com',
      port: 443,
      path: '/v1alpha/sessions',
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + JULES_API_KEY }
    };

    const req = https.request(options, (response) => {
      let body = '';
      response.on('data', chunk => body += chunk);
      response.on('end', () => {
        if (response.statusCode === 200) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error('Jules API error: ' + response.statusCode + ' - ' + body));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function getJulesSession(sessionId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'jules.googleapis.com',
      port: 443,
      path: '/v1alpha/sessions/' + sessionId,
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + JULES_API_KEY }
    };

    const req = https.request(options, (response) => {
      let body = '';
      response.on('data', chunk => body += chunk);
      response.on('end', () => {
        if (response.statusCode === 200) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error('Jules API error: ' + response.statusCode + ' - ' + body));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
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
