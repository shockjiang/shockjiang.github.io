## Project: shockjiang.github.io — Personal Academic Homepage

### Architecture
- **Single-page Jekyll site** hosted on GitHub Pages
- All content in `_data/` YAML files, rendered by Liquid templates in `_includes/`
- Vanilla JS for interactivity (no frameworks)
- `_build.py` generates a static HTML preview for local dev (Ruby/Jekyll too new to run locally)
- Old site preserved in `old/` (excluded from build, do not modify)

### File Structure
```
_config.yml              # Jekyll config (excludes old/, docs/, data/)
Gemfile                   # Jekyll 4 + plugins
index.html                # Single page entry (layout: default)
_layouts/default.html     # HTML shell: profile orbit, nav, panels, visitor stats, footer
_includes/
  profile.html            # Orbit layout with 3 tag rings + center card
  news.html               # News items (bilingual)
  publications.html       # Tag filter bar + year-grouped papers with venue badges
  projects.html           # Project cards with video/image galleries
  cv.html                 # CV (bilingual EN/ZH)
_data/
  profile.yml             # Name, title, bio, links, experience_tags, skill_tags (with name_zh, tip, link)
  news.yml                # News items (date + en/zh content, supports HTML links)
  publications.yml        # All papers: title, authors, venue, year, url, arxiv, pdf, tags
  projects.yml            # Project cards: title, subtitle, desc, tags, videos, images, links
  cv_en.yml / cv_zh.yml   # CV: education, work, skills, hobbies (structured YAML)
assets/
  css/style.scss          # All CSS: orbit animations, themes, panels, responsive
  js/main.js              # Panel toggle, lang switch, tag filter, orbit layout, tooltips, theme
  images/profile.png      # Avatar
files/                    # PDF papers
_build.py                 # Python script for local preview (generates _site/index.html)
```

### Key Features
1. **Orbit profile** — tags orbit around center card in 2 ellipses (inner=experience, outer=skills+research). Tags have glow/drift animations, tooltips with associated data, and click-to-navigate.
2. **4 panels** — Publications (default), News, Projects, CV. Smooth fade-in transitions.
3. **Bilingual** — EN/ZH toggle. Orbit tags also switch language. Orbit re-layouts on language change.
4. **Tag system** — Publications tagged and filterable. Research tags in orbit link to Publications panel with auto-filter.
5. **5 color themes** — dark (default), midnight, ocean, warm, light. Persisted in localStorage.
6. **Venue badges** — ORAL (green) and TOP (purple) badges on publications. First-author/corresponding papers highlighted with orange left border.
7. **Projects** — DINO-XGrasp (Bilibili iframe embeds), oVP (image gallery from aliyuncs CDN).
8. **Visitor stats** — busuanzi counter + jsvectormap world map (jsDelivr CDN).

### Local Development
```bash
# Ruby is too new (4.0) for github-pages gem, so use Python preview:
python3 _build.py              # builds to _site/index.html
cd _site && python3 -m http.server 4000   # serve at localhost:4000

# Note: proxy may interfere with curl, but browser access works fine
```

### Deployment
- Push to `master` branch
- GitHub Actions workflow (`.github/workflows/jekyll.yml`) builds with Ruby 3.1 and deploys

### Important Notes
- `_build.py` and Jekyll templates must stay in sync — both render the same page
- `_build.py` uses `libsass` (Python `sass` module) to compile SCSS → CSS. Raw SCSS inlined as `<style>` will break nested selectors in browsers.
- `publications.yml` uses `year` field for grouping — use the publication/acceptance year, not submission year
- Experience/skill tags in `profile.yml` have `name`, `name_zh`, `tip`, `link` fields
- Research tags are auto-derived from `publications.yml` tags
- Orbit layout JS runs on DOMContentLoaded and window resize, also re-runs after language toggle
- `pointer-events: none` on `.orbit-ring` is critical — without it, orbit rings block profile center links
- The `profile-center` frosted glass card uses hardcoded rgba, not CSS var — intentional for dark themes
- **Chinese is default language**: `data-lang="zh"` spans are visible, `data-lang="en"` has `style="display:none"`. When adding bilingual content, ZH is shown first.
- RevolverMaps was removed (unreachable from China), replaced with busuanzi + jsvectormap
- Papers before 2021 are hidden by default — toggled via "Show earlier papers" button
- Each paper has a BibTeX toggle with copy button
- If a paper has an `arxiv` link, don't set `pdf` — arXiv serves as the primary access
- Project iframes lazy-load via `data-src`, activated when Projects panel is shown

### Gotchas
- **Dual build sync**: Every change to `_includes/`, `_layouts/`, or `assets/` MUST also be applied to `_build.py`. They render the same page independently. Forgetting one causes silent drift.
- **Paper thumbnails**: Check in order: (1) arxiv HTML `https://arxiv.org/html/{id}v1/x1.png`, (2) ar5iv `https://ar5iv.labs.arxiv.org/html/{id}/assets/figures/fig1.png`, (3) project page, (4) GitHub README, (5) extract from local PDF via `pdf2image`. ResearchGate/IEEE block automated access.

### Content Quick Reference
- **Add a paper**: append to `_data/publications.yml` with title, authors, venue, year, url, arxiv, pdf, image, code, project, tags
- **Add news**: prepend to `_data/news.yml` (newest first), supports HTML in content
- **Add a project**: append to `_data/projects.yml` with videos (bilibili embed or mp4) and/or images
- **Add a Bilibili video**: Use `poster` field in projects.yml pointing to a local cover image (`assets/images/videos/`). Download covers via `curl -s "https://api.bilibili.com/x/web-interface/view?bvid=BVID"` and extract `.data.pic`. Embed uses `data-src` (lazy) with `autoplay=1`.
- **Add a tag**: just use it in publications.yml — it auto-appears in orbit and filter bar
- **Mark corresponding author**: use `<strong>Xiaoke Jiang*</strong>` in authors field
- **Add CV logo**: Add `logo: assets/images/logos/name.png` to education/work entry in cv_en.yml and cv_zh.yml. Use `logos: [path1, path2]` for dual logos. Images should have white background (`padding: 3px; background: #fff`).
