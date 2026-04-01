#!/usr/bin/env python3
"""Build static HTML from Jekyll data files for local preview."""
import yaml, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, '_site')

def load(name):
    with open(os.path.join(ROOT, '_data', name)) as f:
        return yaml.safe_load(f)

def read(name):
    with open(os.path.join(ROOT, name)) as f:
        return f.read()

profile = load('profile.yml')
news = load('news.yml')
pubs = load('publications.yml')
cv_en = load('cv_en.yml')
cv_zh = load('cv_zh.yml')
projects = load('projects.yml')
css = read('assets/css/style.scss').split('---')[-1]  # strip frontmatter
js = read('assets/js/main.js')

# Icon SVGs
icons = {
    'scholar': '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M5.242 13.769L0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/></svg>',
    'github': '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>',
    'zhihu': '<svg viewBox="0 0 1024 1024" width="22" height="22" fill="currentColor"><path d="M564.7 230.1V803h-60.3l-20.2 60.8-149.2-60.8H134.8V230.1h429.9zm-404.2 36v500.6h155.5l94.2 38.4 12.7-38.4h105.7V266.1H160.5zm579.9-111.6l27 31.4-41.8 36 27.6 32.2-41.8 35.6 27.6 32.2L697.2 358l27.6 32.2-84.4 72.2V803H480.7V200.2h138.8L556 128.5h88.4zm-23.5 220.8l42.2-36.2-55.2-64.4 42.2-36.2-55.2-64.4 42.2-36.2-55.2-64.4h159.8V803h-121V375.3zm263.4 0V803H859V375.3h121.3z"/></svg>',
    'email': '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>',
}

def profile_tags_html():
    all_tags = []
    for p in pubs:
        for t in p.get('tags', []):
            if t not in all_tags:
                all_tags.append(t)
    return '\n'.join(f'<span class="profile-tag">{t}</span>' for t in all_tags)

def profile_links_html():
    parts = []
    for link in profile['links']:
        icon = icons.get(link['icon'], '')
        parts.append(f'<a href="{link["url"]}" class="profile-link" title="{link["name"]}" target="_blank" rel="noopener">{icon}</a>')
    return '\n'.join(parts)

def news_html():
    parts = []
    for item in news:
        parts.append(f'''<div class="news-item">
    <span class="news-date">{item['date']}</span>
    <span class="news-content">
      <span data-lang="en">{item['content']['en']}</span>
      <span data-lang="zh" style="display:none">{item['content']['zh']}</span>
    </span>
  </div>''')
    return '\n'.join(parts)

def pubs_html():
    # Collect unique tags
    all_tags = []
    for p in pubs:
        for t in p.get('tags', []):
            if t not in all_tags:
                all_tags.append(t)

    tag_btns = '<button class="tag-btn active" data-tag="all">All</button>\n'
    for t in all_tags:
        tag_btns += f'  <button class="tag-btn" data-tag="{t}">{t}</button>\n'

    items = []
    current_year = 0
    for p in pubs:
        if p['year'] != current_year:
            current_year = p['year']
            items.append(f'<h3 class="pub-year">{current_year}</h3>')

        tags_str = '||'.join(p.get('tags', []))
        tag_spans = ''.join(f'<span class="pub-tag">{t}</span>' for t in p.get('tags', []))
        title_html = f'<a href="{p["url"]}" target="_blank" rel="noopener">{p["title"]}</a>' if p.get('url') else f'<span class="pub-title">{p["title"]}</span>'
        arxiv_html = f' <a href="{p["arxiv"]}" class="pub-pdf" target="_blank" rel="noopener">[arXiv]</a>' if p.get('arxiv') else ''
        pdf_html = f' <a href="{p["pdf"]}" class="pub-pdf" target="_blank" rel="noopener">[PDF]</a>' if p.get('pdf') else ''

        items.append(f'''<div class="pub-item" data-tags="{tags_str}">
      <p>{tag_spans}{p['authors']}, {title_html}, <em>{p['venue']}</em>.{arxiv_html}{pdf_html}</p>
    </div>''')

    return f'<div class="tag-bar">\n  {tag_btns}</div>\n<div class="pub-list">\n' + '\n'.join(items) + '\n</div>'

def cv_section_html(cv, labels):
    parts = []
    parts.append(f'<h2 class="cv-section-title">{labels["edu"]}</h2>')
    for edu in cv['education']:
        deg = f' &mdash; {edu["degree"]}' if edu.get('degree') else ''
        sup = f'<div class="cv-supervisor">{labels["sup"]}: {edu["supervisor"]}</div>' if edu.get('supervisor') else ''
        details = ''
        if edu.get('details'):
            details = '<ul class="cv-details">' + ''.join(f'<li>{d}</li>' for d in edu['details']) + '</ul>'
        parts.append(f'''<div class="cv-entry">
    <div class="cv-period">{edu['period']}</div>
    <div class="cv-body">
      <div class="cv-heading">{edu['institution']}{deg}</div>
      {sup}{details}
    </div>
  </div>''')

    parts.append(f'<h2 class="cv-section-title">{labels["work"]}</h2>')
    for job in cv['work']:
        highlights = []
        for h in job.get('highlights', []):
            desc = f': {h["desc"]}' if h.get('desc') else ''
            demos = ''
            if h.get('demos'):
                demo_links = ' | '.join(f'<a href="{d["url"]}" target="_blank" rel="noopener">{d["text"]}</a>' for d in h['demos'])
                demos = f'<div class="cv-demos">{demo_links}</div>'
            highlights.append(f'<div class="cv-highlight"><strong>{h["title"]}</strong>{desc}{demos}</div>')

        parts.append(f'''<div class="cv-entry">
    <div class="cv-period">{job['period']}</div>
    <div class="cv-body">
      <div class="cv-heading"><a href="{job.get('url','#')}" target="_blank" rel="noopener">{job['company']}</a> &mdash; {job['role']}</div>
      {''.join(highlights)}
    </div>
  </div>''')

    parts.append(f'<h2 class="cv-section-title">{labels["skills"]}</h2>')
    for s in cv.get('skills', []):
        parts.append(f'<div class="cv-skill"><strong>{s["category"]}:</strong> {" / ".join(s["items"])}</div>')

    parts.append(f'<h2 class="cv-section-title">{labels["hobbies"]}</h2>')
    parts.append(f'<p class="cv-hobbies">{" &bull; ".join(cv.get("hobbies", []))}</p>')
    return '\n'.join(parts)

def projects_html():
    parts = []
    for proj in projects:
        tag_spans = ''.join(f'<span class="pub-tag">{t}</span>' for t in proj.get('tags', []))
        links_html = ''
        if proj.get('links'):
            link_items = ' | '.join(f'<a href="{l["url"]}" target="_blank" rel="noopener">{l["text"]}</a>' for l in proj['links'])
            links_html = f'<div class="project-links">{link_items}</div>'
        videos = []
        for v in proj.get('videos', []):
            videos.append(f'''<div class="project-video">
        <div class="video-wrap"><iframe src="{v['embed']}" allowfullscreen scrolling="no" frameborder="0"></iframe></div>
        <span class="video-label">{v['title']}</span>
      </div>''')
        parts.append(f'''<div class="project-card">
  <div class="project-header">
    <h3 class="project-title">{proj['title']}</h3>
    <span class="project-subtitle">{proj.get('subtitle','')}</span>
  </div>
  <div class="project-tags">{tag_spans}</div>
  <p class="project-desc">{proj['description']}</p>
  {links_html}
  <div class="project-videos">
    {''.join(videos)}
  </div>
</div>''')
    return '\n'.join(parts)

en_labels = {'edu': 'Education', 'work': 'Work Experience', 'skills': 'Skills', 'hobbies': 'Hobbies', 'sup': 'Supervisor'}
zh_labels = {'edu': '教育经历', 'work': '工作经历', 'skills': '技能', 'hobbies': '爱好', 'sup': '导师'}

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{profile['name']['en']}</title>
  <style>{css}</style>
</head>
<body>
  <main class="container">
    <div class="profile">
      <img src="assets/images/profile.png" alt="avatar" class="avatar">
      <h1 class="profile-name">
        <span data-lang="en">{profile['name']['en']}</span>
        <span data-lang="zh" style="display:none">{profile['name']['zh']}</span>
      </h1>
      <p class="profile-title">
        <span data-lang="en">{profile['title']['en']}</span>
        <span data-lang="zh" style="display:none">{profile['title']['zh']}</span>
      </p>
      <p class="profile-bio">
        <span data-lang="en">{profile['bio']['en']}</span>
        <span data-lang="zh" style="display:none">{profile['bio']['zh']}</span>
      </p>
      <div class="profile-links">
        {profile_links_html()}
      </div>
      <div class="profile-tags experience-tags">
        {''.join(f'<span class="profile-tag exp-tag">{t}</span>' for t in profile.get('experience_tags', []))}
      </div>
      <div class="profile-tags skill-tags">
        {''.join(f'<span class="profile-tag skill-tag">{t}</span>' for t in profile.get('skill_tags', []))}
      </div>
      <div class="profile-tags research-tags">
        {profile_tags_html()}
      </div>
    </div>

    <nav class="panel-nav">
      <div class="panel-links">
        <a href="#" data-panel="news" class="active">News</a>
        <a href="#" data-panel="publications">Publications</a>
        <a href="#" data-panel="projects">Projects</a>
        <a href="#" data-panel="cv">CV</a>
      </div>
      <div class="theme-dots">
        <span class="theme-dot" data-theme="dark" title="Dark"></span>
        <span class="theme-dot" data-theme="midnight" title="Midnight"></span>
        <span class="theme-dot" data-theme="ocean" title="Ocean"></span>
        <span class="theme-dot" data-theme="warm" title="Warm"></span>
        <span class="theme-dot" data-theme="light" title="Light"></span>
      </div>
      <div class="lang-toggle">
        <a href="#" data-lang-btn="en" class="active">EN</a>
        <span class="sep">|</span>
        <a href="#" data-lang-btn="zh">中文</a>
      </div>
    </nav>

    <section id="panel-news" class="panel active">
      <div class="news-list">
        {news_html()}
      </div>
    </section>

    <section id="panel-publications" class="panel">
      {pubs_html()}
    </section>

    <section id="panel-projects" class="panel">
      {projects_html()}
    </section>

    <section id="panel-cv" class="panel">
      <div data-lang="en">
        {cv_section_html(cv_en, en_labels)}
      </div>
      <div data-lang="zh" style="display:none">
        {cv_section_html(cv_zh, zh_labels)}
      </div>
    </section>
  </main>

  <div class="visitor-stats">
    <div class="visitor-title">Visitors</div>
    <div class="visitor-globe">
      <script type="text/javascript" src="//rf.revolvermaps.com/0/0/8.js?i=5e4x5w2ajfs&amp;m=0&amp;c=ff0000&amp;cr1=ffffff&amp;f=arial&amp;l=33&amp;bv=80&amp;lx=-420&amp;ly=420&amp;hi=8&amp;he=2&amp;hc=34d399&amp;rs=20" async="async"></script>
    </div>
  </div>

  <footer class="footer">
    <p>&copy; 2025 Shock (Xiaoke) Jiang</p>
  </footer>

  <script>{js}</script>
</body>
</html>'''

os.makedirs(SITE, exist_ok=True)
with open(os.path.join(SITE, 'index.html'), 'w') as f:
    f.write(html)

# Copy assets
for d in ['assets/images', 'files']:
    src = os.path.join(ROOT, d)
    dst = os.path.join(SITE, d)
    if os.path.exists(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)

print(f"Built to {SITE}/index.html")
