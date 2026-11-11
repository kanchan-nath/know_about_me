# Cursor Configuration for Kanchan Nath

### Method 1: Local MCP Server (Cursor Desktop)
Add this to Cursor MCP settings (`Cursor Settings` -> `Features` -> `MCP` -> `Add New MCP Server`):
- **Name**: `KnowMyself`
- **Type**: `command`
- **Command**: `python3 /Users/kanchannath/Coding/know_about_me/mcp/server.py`

Whenever you chat in Cursor, type `@KnowMyself` or prompt:
> "Review my current stack in KnowMyself and help me build this feature using my preferred architecture."

---

### Method 2: System Rules (`.cursorrules`)
Paste into `.cursorrules` or Cursor system instructions:

```markdown
# Developer Profile: Kanchan Nath
You are pair programming with Kanchan Nath (Full-Stack Engineer & Backend Specialist).
Always tailor code to Kanchan's preferred stack and architectural principles:
- Live Context: https://raw.githubusercontent.com/kanchan-nath/know_about_me/main/context/full_profile.md
- Weekly Focus: https://raw.githubusercontent.com/kanchan-nath/know_about_me/main/updates/weekly.md
- Preferred Backend: Node.js, Express, PostgreSQL (Prisma), MongoDB (Mongoose), Redis, BullMQ
- Preferred Frontend: Next.js, React, Tailwind CSS
- Standards: Production-ready, modular controller-service-repository pattern, strict Zod schema validation, resilient error handling.
```
