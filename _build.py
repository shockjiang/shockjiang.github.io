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
    'zhihu': '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M5.721 0C2.251 0 0 2.25 0 5.719V18.28C0 21.751 2.252 24 5.721 24h12.56C21.751 24 24 21.75 24 18.281V5.72C24 2.249 21.75 0 18.281 0zm1.964 4.078c-.271.73-.5 1.434-.68 2.11h4.587c.545-.006.445 1.168.445 1.171H9.384a58.104 58.104 0 01-.112 3.797h2.712c.388.023.393 1.251.393 1.266H9.183a9.223 9.223 0 01-.408 2.102l.757-.604c.452.456 1.512 1.712 1.906 2.177.473.681.063 2.081.063 2.081l-2.794-3.382c-.653 2.518-1.845 3.607-1.845 3.607-.523.468-1.58.82-2.64.516 2.218-1.73 3.44-3.917 3.667-6.497H4.491c0-.015.197-1.243.806-1.266h2.71c.024-.32.086-3.254.086-3.797H6.598c-.136.406-.158.447-.268.753-.594 1.095-1.603 1.122-1.907 1.155.906-1.821 1.416-3.6 1.591-4.064.425-1.124 1.671-1.125 1.671-1.125zM13.078 6h6.377v11.33h-2.573l-2.184 1.373-.401-1.373h-1.219zm1.313 1.219v8.86h.623l.263.937 1.455-.938h1.456v-8.86z"/></svg>',
    'email': '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>',
}

def profile_tags_html_orbit():
    all_tags = []
    tag_tips = {}
    for p in pubs:
        for t in p.get('tags', []):
            if t not in all_tags:
                all_tags.append(t)
                tag_tips[t] = []
            tag_tips[t].append(p['title'])
    parts = []
    for t in all_tags:
        tip = '; '.join(tag_tips[t])
        if len(tip) > 120:
            tip = tip[:117] + '...'
        tip_escaped = tip.replace('"', '&quot;')
        parts.append(f'<span class="profile-tag orbit-tag" data-tooltip="{tip_escaped}" data-link="publications">{t}</span>')
    return '\n'.join(parts)

def profile_tags_html():
    all_tags = []
    for p in pubs:
        for t in p.get('tags', []):
            if t not in all_tags:
                all_tags.append(t)
    return '\n'.join(f'<span class="profile-tag">{t}</span>' for t in all_tags)

def exp_tags_html():
    return '\n'.join(
        '<span class="profile-tag exp-tag orbit-tag" data-tooltip="{tip}" data-link="{link}"><span data-lang="en">{name}</span><span data-lang="zh" style="display:none">{name_zh}</span></span>'.format(
            tip=t['tip'].replace('"', '&quot;'), name=t['name'], name_zh=t.get('name_zh', t['name']), link=t.get('link', 'cv')
        ) for t in profile.get('experience_tags', [])
    )

def skill_tags_html():
    return '\n'.join(
        '<span class="profile-tag skill-tag orbit-tag" data-tooltip="{tip}" data-link="cv"><span data-lang="en">{name}</span><span data-lang="zh" style="display:none">{name_zh}</span></span>'.format(
            tip=t['tip'].replace('"', '&quot;'), name=t['name'], name_zh=t.get('name_zh', t['name'])
        ) for t in profile.get('skill_tags', [])
    )

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

        is_highlight = 'Xiaoke Jiang*' in p['authors'] or 'Xiaoke Jiang</strong>,' in p['authors']
        venue = p.get('venue', '')
        is_oral = 'Oral' in venue
        hl_class = ' pub-item--oral' if is_oral else (' pub-item--highlight' if is_highlight else '')
        venue_badge = ''
        if is_oral:
            venue_badge = ' <span class="venue-badge venue-badge--oral">ORAL</span>'
        elif any(v in venue for v in ['CVPR', 'ICCV', 'AAAI', 'IJCAI', 'SIGCOMM', 'ICNP']):
            venue_badge = ' <span class="venue-badge venue-badge--top">TOP</span>'
        items.append(f'''<div class="pub-item{hl_class}" data-tags="{tags_str}">
      <p>{tag_spans}{p['authors']}, {title_html}, <em>{p['venue']}</em>.{venue_badge}{arxiv_html}{pdf_html}</p>
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
        images_html = ''
        if proj.get('images'):
            img_items = []
            for img in proj['images']:
                img_items.append(f'''<div class="project-image">
      <a href="{img['url']}" target="_blank" rel="noopener"><img src="{img['url']}" alt="{img['title']}" loading="lazy"></a>
      <span class="video-label">{img['title']}</span>
    </div>''')
            images_html = f'<div class="project-gallery">{"".join(img_items)}</div>'
        videos = []
        for v in proj.get('videos', []):
            if v.get('type') == 'video':
                media = f'<video src="{v["url"]}" controls muted playsinline preload="metadata"></video>'
            else:
                media = f'<iframe src="{v["embed"]}" allowfullscreen scrolling="no" frameborder="0"></iframe>'
            videos.append(f'''<div class="project-video">
        <div class="video-wrap">{media}</div>
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
  {images_html}
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
  <link rel="icon" href="assets/images/favicon.png" type="image/png">
  <style>{css}</style>
</head>
<body>
  <main class="container">
    <div class="profile">
      <div class="profile-orbit">
        <div class="orbit-ring orbit-inner">
          {exp_tags_html()}
        </div>
        <div class="orbit-ring orbit-outer">
          {skill_tags_html()}
          {profile_tags_html_orbit()}
        </div>
        <div class="profile-center">
          <picture>
            <source srcset="assets/images/profile.webp" type="image/webp">
            <img src="assets/images/profile.png" alt="avatar" class="avatar">
          </picture>
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
          <p class="profile-statement">
            <span data-lang="en">{profile['statement']['en'].replace(chr(10), '<br>')}</span>
            <span data-lang="zh" style="display:none">{profile['statement']['zh'].replace(chr(10), '<br>')}</span>
          </p>
          <div class="profile-links">
            {profile_links_html()}
          </div>
          <div class="profile-stats">
            <div class="profile-stat"><span class="stat-num">{len(pubs)}</span><div class="stat-label">Papers</div></div>
            <div class="profile-stat"><span class="stat-num">10+</span><div class="stat-label">First Author</div></div>
            <div class="profile-stat"><span class="stat-num">10+</span><div class="stat-label">Corresponding</div></div>
          </div>
        </div>
      </div>
    </div>

    <nav class="panel-nav">
      <div class="panel-links">
        <a href="#" data-panel="news">News</a>
        <a href="#" data-panel="publications" class="active">Publications</a>
        <a href="#" data-panel="projects">Projects</a>
        <a href="#" data-panel="cv">Resume</a>
      </div>
      <span class="nav-divider"></span>
      <div class="theme-dots">
        <span class="theme-dot" data-theme="dark" title="Dark"></span>
        <span class="theme-dot" data-theme="midnight" title="Midnight"></span>
        <span class="theme-dot" data-theme="ocean" title="Ocean"></span>
        <span class="theme-dot" data-theme="warm" title="Warm"></span>
        <span class="theme-dot" data-theme="light" title="Light"></span>
      </div>
      <span class="nav-divider"></span>
      <div class="lang-toggle">
        <a href="#" data-lang-btn="en" class="active">EN</a>
        <span class="sep">|</span>
        <a href="#" data-lang-btn="zh">中文</a>
      </div>
    </nav>

    <section id="panel-news" class="panel">
      <div class="news-list">
        {news_html()}
      </div>
    </section>

    <section id="panel-publications" class="panel active">
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
    <div class="visitor-counters">
      <div class="visitor-counter">
        <span class="counter-num" id="busuanzi_value_site_uv">--</span>
        <span class="counter-label">Visitors</span>
      </div>
      <div class="visitor-counter">
        <span class="counter-num" id="busuanzi_value_site_pv">--</span>
        <span class="counter-label">Page Views</span>
      </div>
    </div>
    <div id="visitor-map" class="visitor-map"></div>
    <script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jsvectormap/dist/css/jsvectormap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/jsvectormap"></script>
    <script src="https://cdn.jsdelivr.net/npm/jsvectormap/dist/maps/world.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function() {{
        if (document.getElementById('visitor-map') && typeof jsVectorMap !== 'undefined') {{
          var isDark = !document.documentElement.getAttribute('data-theme') ||
                       document.documentElement.getAttribute('data-theme') !== 'light';
          new jsVectorMap({{
            selector: '#visitor-map',
            map: 'world',
            backgroundColor: 'transparent',
            draggable: true,
            zoomButtons: false,
            zoomOnScroll: false,
            regionStyle: {{
              initial: {{
                fill: isDark ? '#1a1a2e' : '#d1d5db',
                stroke: isDark ? '#2a2a4a' : '#9ca3af',
                strokeWidth: 0.4
              }},
              hover: {{
                fill: '#34d399',
                cursor: 'pointer'
              }}
            }}
          }});
        }}
      }});
    </script>
  </div>

  <footer class="footer">
    <p>&copy; {__import__('datetime').date.today().year} Shock (Xiaoke) Jiang &middot; Built with Jekyll &middot; Hosted on GitHub Pages</p>
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
