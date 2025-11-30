# Antigravity-Jules Orchestration

## Overview
Autonomous AI orchestration architecture combining **Google Antigravity** with the **Jules API** for hands-free development workflows. This system leverages the Model Context Protocol (MCP) for seamless agent coordination.

## Architecture Components

### 1. Google Antigravity Integration
- **Browser Subagent**: Specialized model for browser automation with DOM capture, screenshots, and video recording
- **Agent Modes**: Planning mode for complex tasks with task groups and artifacts; Fast mode for simple operations
- **Workspace Management**: Multi-workspace support with parallel conversation execution
- **Task Lists & Implementation Plans**: Structured approach to complex tasks with approval workflows
- **MCP Store Integration**: Built-in support for connecting to external services and databases

### 2. Jules API Connection
- **Autonomous Coding Sessions**: Create and manage Jules coding sessions directly from AI assistants
- **GitHub Integration**: Connect to repositories through Jules sources
- **Plan Approval Workflow**: Review and approve execution plans before changes
- **Real-time Activity Tracking**: Monitor session progress with detailed activity logs
- **MCP Bridge**: Jules MCP server acts as bridge between AI assistants and Jules API

### 3. MCP Integration Layer
- **Custom MCP Server**: Node.js-based server using Streamable HTTP transport
- **Type-safe Validation**: Zod schemas for runtime validation of all inputs
- **Stateless Architecture**: Optimized for compatibility with multiple MCP clients
- **Tools Available**:
  - `jules_list_sources` - List connected GitHub sources
  - `jules_create_session` - Create new coding sessions
  - `jules_list_sessions` - List all sessions
  - `jules_approve_plan` - Approve execution plans
  - `jules_send_message` - Send messages to active agents
  - `jules_list_activities` - Monitor session activities

## Workflow Architecture

### Autonomous Development Loop
1. **Task Initiation**: User provides high-level task in Antigravity
2. **Planning Phase**: Antigravity agent creates implementation plan with task groups
3. **Jules Session Creation**: MCP server creates Jules coding session with appropriate source
4. **Parallel Execution**: 
   - Antigravity manages browser automation and UI interactions
   - Jules handles code generation and repository modifications
5. **Progress Monitoring**: Real-time activity tracking across both systems
6. **Approval Gates**: Implementation plans reviewed before execution
7. **Completion**: Changes merged, tests executed, documentation updated

### Key Advantages
- **Minimal User Interruption**: Autonomous execution with approval gates only for critical decisions
- **Parallel Processing**: Multiple workspaces and sessions running simultaneously
- **Browser + Code Coordination**: Antigravity handles web tasks while Jules manages code
- **Type Safety**: Zod validation prevents invalid API calls
- **Persistent Sessions**: MCP server runs as HTTP service for reliability

## Installation

### Prerequisites
- Node.js v18+
- Google Antigravity installed ([download](https://antigravity.google/download))
- Jules API account with API key
- GitHub account with connected repositories

### Setup Steps

1. **Clone Repository**
```bash
git clone https://github.com/Scarmonit/antigravity-jules-orchestration.git
cd antigravity-jules-orchestration
```

2. **Install Dependencies**
```bash
npm install
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add:
# JULES_API_KEY=your_api_key_here
# PORT=3323
# HOST=127.0.0.1
```

4. **Start MCP Server**
```bash
npm run dev
```

5. **Configure Antigravity**
- Open Antigravity
- Navigate to Agent Manager → MCP Servers
- Add configuration:
```json
{
  "mcpServers": {
    "jules": {
      "type": "streamable-http",
      "url": "http://127.0.0.1:3323/mcp"
    }
  }
}
```

## Usage Examples

### Example 1: Create Coding Session
```
Prompt: "List my Jules sources and create a session for my main repository to add authentication"
```

Antigravity will:
1. Call `jules_list_sources` to show available repositories
2. Call `jules_create_session` with the task prompt
3. Display session details and activity updates

### Example 2: Multi-Agent Workflow
```
Prompt: "Research best practices for API rate limiting, then implement it in my Jules session"
```

Antigravity will:
1. Use Browser Subagent to research rate limiting patterns
2. Create artifacts with findings
3. Send research context to Jules session via MCP
4. Jules implements the solution with approval workflow

### Example 3: Monitoring and Approval
```
Prompt: "Show me the latest activities from session sessions/abc123 and approve the plan if it looks good"
```

Antigravity will:
1. Call `jules_list_activities` to fetch recent actions
2. Display activities for user review
3. Call `jules_approve_plan` to proceed with execution

## Configuration

### Antigravity Settings
- **Agent Mode**: Use Planning mode for complex orchestration tasks
- **Artifact Review Policy**: Set to "Agent Decides" for balanced automation
- **Terminal Auto Execution**: Configure allow/deny lists for safe automation

### Jules MCP Server
- **Transport**: Streamable HTTP (required for Antigravity)
- **Validation**: All inputs validated with Zod before API calls
- **CORS**: Configure `ALLOWED_ORIGINS` for security

## Integration Opportunities

### With Existing Jules API System
- Connect to existing ScarMonit Dashboard for monitoring
- Integrate with Docker containerization workflows
- Leverage Tailscale for secure remote access
- Coordinate with other AI services (Claude, Gemini, ChatGPT)

### Future Enhancements
- Multi-repository orchestration across workspaces
- Automated testing integration with Jules sessions
- CI/CD pipeline integration for deployment automation
- Browser recording artifacts for documentation
- Knowledge base integration for context persistence

## Troubleshooting

### MCP Server Connection Issues
- Verify server is running: `curl http://127.0.0.1:3323/mcp`
- Check JULES_API_KEY is set correctly
- Ensure port 3323 is not in use
- Restart Antigravity after configuration changes

### Tool Call Failures
- Check validation error messages for specific field requirements
- Verify session IDs match format `sessions/{id}`
- Ensure source paths match format `sources/github/owner/repo`

## Resources

- [Google Antigravity Documentation](https://antigravity.google/docs)
- [Jules API Documentation](https://developers.google.com/jules/api)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Jules MCP Server Reference](https://github.com/GatienBoquet/jules_mcp)

## License
MIT License

## Contact
- Email: Scarmonit@gmail.com
- GitHub: [@Scarmonit](https://github.com/Scarmonit)
