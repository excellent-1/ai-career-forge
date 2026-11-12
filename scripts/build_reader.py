"""Embed shared chapter content into a portable, buildless HTML reader."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from career_forge.analyzer import SKILLS

content = (ROOT/'content/chapter1.json').read_text()
chapter = json.loads(content)
(ROOT/'docs/chapter-01.md').write_text('# Chapter 1 — Build a Job Requirements Analyzer\n\n' + '\n\n---\n\n'.join('## '+lesson['title']+'\n\n'+lesson['body'] for lesson in chapter['lessons']))
skills = json.dumps(SKILLS)
# Escaping < prevents embedded content from terminating a script element.
content = content.replace('<','\\u003c')
skills = skills.replace('<','\\u003c')
html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Build a deployable AI job requirements analyzer. Interactive lessons, coding practice, evidence checks, and portfolio milestones."><title>AI Career Forge — Chapter 1</title><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#workspace">Skip to chapter content</a>
<aside><div class="brand"><span>F</span> AI Career Forge</div><div class="eyebrow">An engineering fieldbook</div><nav id="nav" aria-label="Chapter navigation"></nav><div class="sidebar-bottom"><label for="progress" id="progress-text">0 / 9 sections marked read</label><progress id="progress" max="9" value="0"></progress><p>Learn with assistance.<br>Validate with evidence.</p></div></aside>
<main><div class="topbar"><span>THE AI ENGINEERING SERIES / CHAPTER 01</span><span class="pill">Working draft · v0.1</span></div>
<header class="hero"><div class="eyebrow">Your first deployable AI system</div><h1>From job posting<br>to structured evidence.</h1><p>Build a Job Requirements Analyzer. Learn the Python, prompts, contracts, and verification behind a system you can explain.</p><div class="actions"><button type="button" class="btn demo-launch" id="run-completed">Run completed Chapter 1 project →</button></div><p class="demo-caption">Try the finished example before you build it.</p><div class="tags"><span class="tag">PYTHON</span><span class="tag">PYDANTIC</span><span class="tag">STRUCTURED OUTPUTS</span><span class="tag">STREAMLIT</span></div></header>
<div class="stats"><div class="stat"><strong>09</strong><span>Focused sections</span></div><div class="stat"><strong>12</strong><span>Practice challenges</span></div><div class="stat"><strong>01</strong><span>Deployable project</span></div></div>
<div class="content-grid"><article id="workspace" class="panel" tabindex="-1"></article><div class="context-column"><section class="right-card"><div class="eyebrow">Chapter outcome</div><h3>Build. Verify. Explain.</h3><ul><li>A typed extraction contract</li><li>An inspectable baseline</li><li>An optional AI adapter</li><li>Evidence verification</li><li>A portfolio release</li></ul></section><section class="right-card dark"><h3>Evidence over confidence.</h3><p>Valid JSON is a beginning. The source must support the claim.</p><p class="small">Use the failure lab to see where simple rules break.</p></section><section class="right-card"><h3>Keep your work</h3><p class="small">Source, tests, a printable chapter, and deployment guides are in the repository. Export progress from the portfolio tab.</p><a href="../docs/chapter-01.md">Read Markdown source ↗</a></section></div></div>
<footer class="footer">AI Career Forge · Original project draft for Nathaniel Hibbler · Chapter 1 implemented; later chapters planned.</footer></main>
<script id="chapter-data" type="application/json">CHAPTER_DATA</script><script id="skill-data" type="application/json">SKILL_DATA</script><script src="app.js"></script></body></html>'''
(ROOT/'web/index.html').write_text(html.replace('CHAPTER_DATA',content).replace('SKILL_DATA',skills))
# Keep this link working when only web/ is deployed to GitHub Pages.
(ROOT/'web/chapter-01.md').write_text((ROOT/'docs/chapter-01.md').read_text())
p = ROOT/'web/index.html'
p.write_text(p.read_text().replace('../docs/chapter-01.md','chapter-01.md'))
print('Built web/index.html from shared content and Python skill registry.')
