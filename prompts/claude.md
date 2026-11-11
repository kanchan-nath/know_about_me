# Claude Configuration (Web & Desktop) for Kanchan Nath

### Method 1: Claude Desktop MCP Server
In `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "know_myself": {
      "command": "python3",
      "args": [
        "/Users/kanchannath/Coding/know_about_me/mcp/server.py"
      ]
    }
  }
}
```

---

### Method 2: Claude Web Projects / System Prompt
In Claude.ai Project instructions:

```markdown
# Developer Context: Kanchan Nath
Before answering technical questions, generating a resume, writing cover letters, or architecting backend systems, fetch live context about me:
- Live Profile Context: https://raw.githubusercontent.com/kanchan-nath/know_about_me/main/context/full_profile.md
- Skills: https://raw.githubusercontent.com/kanchan-nath/know_about_me/main/data/skills.json
- Projects (StudeQ, Nexus, YouTube backend): https://raw.githubusercontent.com/kanchan-nath/know_about_me/main/data/projects.json
- Weekly Focus: https://raw.githubusercontent.com/kanchan-nath/know_about_me/main/updates/weekly.md

Highlight my actual hands-on expertise with Node.js, Express, Redis/BullMQ, PostgreSQL, Prisma, MongoDB, Next.js, and LLM model evaluation. Do not invent technologies outside my stack without confirmation.
```
