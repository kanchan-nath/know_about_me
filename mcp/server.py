#!/usr/bin/env python3
"""
know_about_me MCP Server for Kanchan Nath
Provides tools and resources for Cursor, Claude Desktop, Antigravity, and other MCP clients.
"""

import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
UPDATES_DIR = ROOT_DIR / "updates"
CONTEXT_DIR = ROOT_DIR / "context"

mcp = FastMCP("KnowMyself")


def _read_json(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_file(file_path: Path):
    if not file_path.exists():
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def get_profile() -> str:
    """Retrieve Kanchan Nath's bio, education, contact links, and coding preferences."""
    data = _read_json("profile.json")
    return json.dumps(data, indent=2)


@mcp.tool()
def get_skills(category: str = "") -> str:
    """
    Retrieve technical skills.
    Optional category: languages, backend, frontend, databases_and_orms, queues_caching_and_devops, ai_and_llms, system_architecture.
    """
    data = _read_json("skills.json")
    if category and category in data:
        return json.dumps({category: data[category]}, indent=2)
    return json.dumps(data, indent=2)


@mcp.tool()
def get_projects(status: str = "") -> str:
    """
    Retrieve project portfolio (StudeQ, Nexus Reverse Proxy, YouTube backend, Content Automation, etc.).
    Optional status filter: 'Active', 'Completed'.
    """
    projects = _read_json("projects.json")
    if status and isinstance(projects, list):
        filtered = [p for p in projects if p.get("status", "").lower() == status.lower()]
        return json.dumps(filtered, indent=2)
    return json.dumps(projects, indent=2)


@mcp.tool()
def get_experience() -> str:
    """Retrieve work experience history (StudeQ, Outlier AI)."""
    experience = _read_json("experience.json")
    return json.dumps(experience, indent=2)


@mcp.tool()
def get_articles() -> str:
    """Retrieve published technical writing and architecture deep dives from Hashnode."""
    articles = _read_json("articles.json")
    return json.dumps(articles, indent=2)


@mcp.tool()
def get_weekly_updates() -> str:
    """Retrieve Kanchan's current focus, active builds, and learnings this week."""
    weekly = _read_file(UPDATES_DIR / "weekly.md")
    return weekly if weekly else "No weekly updates recorded yet."


@mcp.tool()
def get_full_context() -> str:
    """Retrieve complete unified profile in Markdown, ideal for resume creation or system prompt injection."""
    full_path = CONTEXT_DIR / "full_profile.md"
    if not full_path.exists():
        return f"# Profile\n{get_profile()}\n\n# Skills\n{get_skills()}\n\n# Projects\n{get_projects()}"
    return _read_file(full_path)


@mcp.resource("myself://profile")
def profile_resource() -> str:
    return _read_file(CONTEXT_DIR / "full_profile.md")


if __name__ == "__main__":
    mcp.run()
