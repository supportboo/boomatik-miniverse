# Boomatik Miniverse - AI Agent Visualization

A pixel world for visualizing and monitoring Boomatik's AI agent team in real-time.

## Live at: team.boomatik.com (coming soon)

## BOO Agent Team

| Agent | Role | ID |
|-------|------|----|
| Claude Opus | Lead AI Architect | `claude-opus` |
| BOO SEO | SEO Specialist | `boo-seo` |
| BOO ADS | PPC Manager | `boo-ads` |
| BOO SOCIAL | Social Media Manager | `boo-social` |
| BOO BRAND | Brand & Design Lead | `boo-brand` |
| BOO LEADS | Lead Capture Specialist | `boo-leads` |
| BOO CONTENT | Content Creator | `boo-content` |

## Quick Start

```bash
npm install
npm run dev
```

- Frontend: http://localhost:5173
- API Server: http://localhost:4321

## Agent States

- `working` - Agent is executing a task
- `thinking` - Agent is processing/planning
- `idle` - Agent is available
- `sleeping` - Agent is offline/paused
- `error` - Agent encountered an issue

## API Endpoints

```bash
# Register/update agent
curl -X POST http://localhost:4321/api/heartbeat \
  -H 'Content-Type: application/json' \
  -d '{"agent": "boo-seo", "name": "BOO SEO", "state": "working"}'

# List all agents
curl http://localhost:4321/api/agents

# Server info
curl http://localhost:4321/api/info

# Send message
curl -X POST http://localhost:4321/api/act \
  -H 'Content-Type: application/json' \
  -d '{"agent": "boo-seo", "action": "speak", "message": "SEO audit complete!"}'
```

## Claude Code Integration

Hooks in `~/.claude/settings.json` automatically update agent state:
- `PreToolUse` → state: `working`
- `PostToolUse` → state: `thinking`
- `Stop` → state: `idle`

## Deployment

For production at team.boomatik.com:
1. `npm run build`
2. Deploy to your preferred hosting (Railway, Vercel, VPS)
3. Point subdomain `team.boomatik.com` to deployment

## Tech Stack

- Vite (frontend)
- @miniverse/core (pixel rendering)
- @miniverse/server (agent API)
- TypeScript

---

Built by [Boomatik](https://boomatik.com) with Claude Code
