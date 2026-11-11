#!/usr/bin/env python3
"""
Now_Myself Build Script
Reads raw data (JSON & Markdown) and generates:
1. context/full_profile.md  -> Clean markdown ready for single-prompt injection or raw URL fetching.
2. llms.txt & llms-full.txt -> Standard discovery format for AI crawlers and agents.
3. dist/                    -> GitHub Pages static site with live API endpoints and UI.
"""

import os
import json
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
UPDATES_DIR = ROOT_DIR / "updates"
CONTEXT_DIR = ROOT_DIR / "context"
DIST_DIR = ROOT_DIR / "dist"
DIST_API_DIR = DIST_DIR / "api"


def load_json(filename):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_markdown(file_path):
    if not file_path.exists():
        return ""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def build_full_profile_markdown(profile, skills, projects, experience, articles, weekly_text):
    md = []
    name = profile.get("name", "Developer")
    headline = profile.get("headline", "")
    summary = profile.get("summary", "")
    status = profile.get("status", "")
    contact = profile.get("contact", {})
    prefs = profile.get("preferences", {})
    edu = profile.get("education", {})

    md.append(f"# Context & Profile: {name}")
    if headline:
        md.append(f"**{headline}** | {profile.get('location', '')}")
    md.append("")
    md.append(f"> **Status**: {status}")
    md.append("")
    md.append("## Professional Summary")
    md.append(summary)
    md.append("")

    # Education
    if edu:
        md.append("## Education")
        md.append(f"- **{edu.get('degree', '')}**")
        md.append(f"  {edu.get('institution', '')} ({edu.get('period', '')}) | **CGPA**: {edu.get('cgpa', '')}")
        md.append("")

    # Contact & Links
    md.append("## Links & Online Presence")
    for k, v in contact.items():
        if v:
            md.append(f"- **{k.capitalize()}**: {v}")
    md.append("")

    # Preferences
    if prefs:
        md.append("## Developer Preferences & Agent Guidance")
        if "preferred_languages" in prefs:
            md.append(f"- **Preferred Languages**: {', '.join(prefs['preferred_languages'])}")
        if "backend_stack" in prefs:
            md.append(f"- **Core Backend Stack**: {', '.join(prefs['backend_stack'])}")
        if "frontend_stack" in prefs:
            md.append(f"- **Core Frontend Stack**: {', '.join(prefs['frontend_stack'])}")
        if "coding_style" in prefs:
            md.append(f"- **Coding Style**: {prefs['coding_style']}")
        if "agent_instruction" in prefs:
            md.append(f"- **Agent Instruction**: {prefs['agent_instruction']}")
        md.append("")

    # Skills
    md.append("## Technical Skills")
    if "languages" in skills:
        md.append("### Programming Languages")
        for lang in skills["languages"]:
            md.append(f"- **{lang.get('name')}** ({lang.get('level', '')}) - {lang.get('years', 0)} yrs")
    if "backend" in skills:
        md.append(f"- **Backend & APIs**: {', '.join(skills['backend'])}")
    if "frontend" in skills:
        md.append(f"- **Frontend & UI**: {', '.join(skills['frontend'])}")
    if "databases_and_orms" in skills:
        md.append(f"- **Databases & ORMs**: {', '.join(skills['databases_and_orms'])}")
    if "queues_caching_and_devops" in skills:
        md.append(f"- **Queues, Caching & DevOps**: {', '.join(skills['queues_caching_and_devops'])}")
    if "ai_and_llms" in skills:
        md.append(f"- **AI & LLMs**: {', '.join(skills['ai_and_llms'])}")
    if "system_architecture" in skills:
        md.append(f"- **System Architecture**: {', '.join(skills['system_architecture'])}")
    md.append("")

    # Experience
    if experience:
        md.append("## Work Experience")
        for exp in experience:
            md.append(f"### {exp.get('role')} @ {exp.get('company')}")
            md.append(f"*{exp.get('period', '')} | {exp.get('location', '')}*")
            md.append(exp.get("description", ""))
            if "achievements" in exp:
                for ach in exp["achievements"]:
                    md.append(f"- {ach}")
            if "skills_used" in exp:
                md.append(f"- **Technologies**: {', '.join(exp['skills_used'])}")
            md.append("")

    # Projects
    md.append("## Key Projects")
    for proj in projects:
        md.append(f"### {proj.get('name')} `[{proj.get('status', 'Active')}]`")
        md.append(f"*{proj.get('role', '')} ({proj.get('period', '')})*")
        md.append(f"{proj.get('summary', '')}")
        if "tech_stack" in proj:
            md.append(f"- **Tech Stack**: {', '.join(proj['tech_stack'])}")
        if "highlights" in proj:
            md.append("- **Key Highlights**:")
            for h in proj["highlights"]:
                md.append(f"  - {h}")
        links = []
        if proj.get("repo_url"):
            links.append(f"[Code Repo]({proj['repo_url']})")
        if proj.get("live_url"):
            links.append(f"[Live Link]({proj['live_url']})")
        if links:
            md.append(f"- **Links**: {' | '.join(links)}")
        md.append("")

    # Technical Writing
    if articles:
        md.append("## Published Technical Articles & Deep Dives")
        for art in articles:
            md.append(f"- [{art.get('title')}]({art.get('url')}) ({art.get('date')})")
            if "topics" in art:
                md.append(f"  *Topics: {', '.join(art['topics'])}*")
        md.append("")

    # Weekly Update
    if weekly_text:
        md.append("## Latest Weekly Focus & Updates")
        md.append(weekly_text)
        md.append("")

    return "\n".join(md)


def build_llms_txt(profile, skills, projects):
    name = profile.get("name", "Developer")
    headline = profile.get("headline", "")
    summary = profile.get("summary", "")
    langs = [lang["name"] for lang in skills.get("languages", [])] if isinstance(skills.get("languages"), list) else []
    return f"""# {name}
> {headline}

## Summary
{summary}

## Primary Tech Stack
{', '.join(langs)}
Backend: Node.js, Express, PostgreSQL, Prisma, MongoDB, Redis, BullMQ
Frontend: React, Next.js, Three.js

## Direct Context Links
- Full Profile: context/full_profile.md
- Skills: data/skills.json
- Projects: data/projects.json
- Experience: data/experience.json
- Articles: data/articles.json
- Weekly Updates: updates/weekly.md
"""


def generate_html(profile, skills, projects, experience, articles, weekly_text):
    name = profile.get("name", "Kanchan Nath")
    headline = profile.get("headline", "Full-Stack Engineer & Backend Specialist")
    summary = profile.get("summary", "")
    status = profile.get("status", "")
    contact = profile.get("contact", {})

    contact_html = " ".join([
        f'<a href="{v}" target="_blank" style="color:#38bdf8; margin-right:1rem; text-decoration:none;">{k.capitalize()}</a>'
        for k, v in contact.items() if v
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} - Context Hub</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: #131b2e;
      --accent: #38bdf8;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --border: #1e293b;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 2.5rem 1rem;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
    }}
    h1 {{ font-size: 2.4rem; color: #fff; }}
    .headline {{ color: var(--accent); font-size: 1.25rem; margin-top: 0.3rem; font-weight: 500; }}
    .badge {{
      display: inline-block;
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #7dd3fc;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      margin-top: 0.75rem;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }}
    h2 {{ color: var(--accent); font-size: 1.35rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.4rem; }}
    .tag {{
      display: inline-block;
      background: #1e293b;
      color: #e2e8f0;
      padding: 0.25rem 0.55rem;
      border-radius: 6px;
      font-size: 0.82rem;
      margin: 0.2rem;
      border: 1px solid #334155;
    }}
    .api-box {{
      background: #050811;
      border: 1px solid var(--border);
      padding: 0.8rem 1rem;
      border-radius: 8px;
      font-family: monospace;
      font-size: 0.88rem;
      margin-top: 0.5rem;
      color: #34d399;
      word-break: break-all;
    }}
    a {{ color: var(--accent); }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{name}</h1>
      <div class="headline">{headline}</div>
      <div class="badge">Status: {status}</div>
      <p style="margin-top: 1rem; color: var(--text-muted); font-size: 1.05rem;">{summary}</p>
      <div style="margin-top: 1rem;">{contact_html}</div>
    </header>

    <div class="card">
      <h2>🤖 Single Source of Truth AI Endpoints</h2>
      <p style="color:var(--text-muted); margin-bottom:0.5rem">Point Cursor, Claude, ChatGPT, or Antigravity to these endpoints:</p>
      <div class="api-box">Full Markdown Profile: <a href="context/full_profile.md">context/full_profile.md</a></div>
      <div class="api-box">JSON Profile API: <a href="api/profile.json">api/profile.json</a></div>
      <div class="api-box">JSON Skills API: <a href="api/skills.json">api/skills.json</a></div>
      <div class="api-box">JSON Projects API: <a href="api/projects.json">api/projects.json</a></div>
      <div class="api-box">JSON All Data API: <a href="api/all.json">api/all.json</a></div>
    </div>

    <div class="card">
      <h2>🛠️ Technical Skills</h2>
      <div style="margin-bottom:0.8rem">
        <strong>Backend & APIs:</strong><br>
        {"".join([f'<span class="tag">{x}</span>' for x in skills.get("backend", [])])}
      </div>
      <div style="margin-bottom:0.8rem">
        <strong>Queues, Caching & DevOps:</strong><br>
        {"".join([f'<span class="tag">{x}</span>' for x in skills.get("queues_caching_and_devops", [])])}
      </div>
      <div>
        <strong>Frontend & Creative:</strong><br>
        {"".join([f'<span class="tag">{x}</span>' for x in skills.get("frontend", [])])}
      </div>
    </div>

    <div class="card">
      <h2>🚀 Key Projects</h2>
      {"".join([f'<div style="margin-bottom:1.2rem; border-left:3px solid var(--accent); padding-left:0.8rem"><strong>{p.get("name")}</strong> <small style="color:var(--accent)">[{p.get("status")}]</small><br><p style="color:var(--text-muted); font-size:0.92rem">{p.get("summary")}</p><small style="color:#64748b">Stack: {", ".join(p.get("tech_stack", []))}</small></div>' for p in projects])}
    </div>

    <div class="card">
      <h2>✍️ Technical Articles & Architecture Notes</h2>
      <ul>
        {"".join([f'<li style="margin-bottom:0.4rem"><a href="{a.get("url")}" target="_blank">{a.get("title")}</a> <small style="color:var(--text-muted)">({a.get("date")})</small></li>' for a in articles])}
      </ul>
    </div>
  </div>
</body>
</html>
"""


def main():
    print("Compiling Now_Myself context hub for Kanchan Nath...")

    # Load data
    profile = load_json("profile.json")
    skills = load_json("skills.json")
    projects = load_json("projects.json")
    experience = load_json("experience.json")
    articles = load_json("articles.json")
    weekly_text = load_markdown(UPDATES_DIR / "weekly.md")

    # Create directories
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DIST_API_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Generate context/full_profile.md
    full_profile_md = build_full_profile_markdown(profile, skills, projects, experience, articles, weekly_text)
    with open(CONTEXT_DIR / "full_profile.md", "w", encoding="utf-8") as f:
        f.write(full_profile_md)
    print("✓ Created context/full_profile.md")

    # 2. Generate llms.txt & llms-full.txt
    llms_txt = build_llms_txt(profile, skills, projects)
    with open(ROOT_DIR / "llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_txt)
    with open(ROOT_DIR / "llms-full.txt", "w", encoding="utf-8") as f:
        f.write(full_profile_md)
    print("✓ Created llms.txt and llms-full.txt")

    # 3. Generate static API JSON files in dist/api/
    with open(DIST_API_DIR / "profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    with open(DIST_API_DIR / "skills.json", "w", encoding="utf-8") as f:
        json.dump(skills, f, indent=2)
    with open(DIST_API_DIR / "projects.json", "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2)
    with open(DIST_API_DIR / "experience.json", "w", encoding="utf-8") as f:
        json.dump(experience, f, indent=2)
    with open(DIST_API_DIR / "articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    all_data = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "articles": articles,
        "weekly_updates": weekly_text,
    }
    with open(DIST_API_DIR / "all.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    print("✓ Created dist/api JSON files")

    # Also copy context/full_profile.md into dist/context/
    (DIST_DIR / "context").mkdir(parents=True, exist_ok=True)
    shutil.copy(CONTEXT_DIR / "full_profile.md", DIST_DIR / "context" / "full_profile.md")
    shutil.copy(ROOT_DIR / "llms.txt", DIST_DIR / "llms.txt")
    shutil.copy(ROOT_DIR / "llms-full.txt", DIST_DIR / "llms-full.txt")

    # 4. Generate dist/index.html
    html_content = generate_html(profile, skills, projects, experience, articles, weekly_text)
    with open(DIST_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✓ Created dist/index.html")

    print("\nBuild complete successfully!")


if __name__ == "__main__":
    main()
