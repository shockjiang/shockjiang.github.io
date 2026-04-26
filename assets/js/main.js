document.addEventListener('DOMContentLoaded', function () {
  // Panel toggling
  function showPanel(panelName) {
    document.querySelectorAll('.panel').forEach(function (p) { p.style.display = 'none'; });
    document.querySelectorAll('.panel-nav a[data-panel]').forEach(function (a) { a.classList.remove('active'); });
    var panel = document.getElementById('panel-' + panelName);
    var navLink = document.querySelector('.panel-nav a[data-panel="' + panelName + '"]');
    if (panel) panel.style.display = 'block';
    if (navLink) navLink.classList.add('active');
    localStorage.setItem('activePanel', panelName);
    if (panelName === 'projects') {
      document.querySelectorAll('#panel-projects iframe[data-src]').forEach(function(iframe) {
        if (!iframe.getAttribute('src')) { iframe.src = iframe.dataset.src; iframe.removeAttribute('data-src'); }
      });
    }
  }

  document.querySelectorAll('.panel-nav a[data-panel]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      showPanel(link.dataset.panel);
    });
  });

  // Restore last panel
  var savedPanel = localStorage.getItem('activePanel');
  if (savedPanel && document.getElementById('panel-' + savedPanel)) {
    showPanel(savedPanel);
  }

  // Language toggling
  document.querySelectorAll('[data-lang-btn]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var lang = btn.dataset.langBtn;
      document.querySelectorAll('[data-lang]').forEach(function (el) {
        if (el.dataset.lang === lang) {
          el.style.display = '';
        } else {
          el.style.display = 'none';
        }
      });
      document.querySelectorAll('[data-lang-btn]').forEach(function (a) { a.classList.remove('active'); });
      btn.classList.add('active');
      // Re-layout orbit since tag widths change
      setTimeout(layoutAllOrbits, 50);
    });
  });

  // Orbit tag positioning.
  // `placed` is shared across rings so outer tags don't land on inner ones.
  function layoutOrbit(selector, radiusX, radiusY, offsetAngle, placed) {
    var container = document.querySelector('.profile-orbit');
    if (!container) return;
    var tags = container.querySelectorAll(selector + ' .orbit-tag');
    var count = tags.length;
    if (!count) return;
    var cx = container.offsetWidth / 2;
    var cy = container.offsetHeight / 2;
    var maxX = container.offsetWidth;
    var maxY = container.offsetHeight;
    // Card bounds — used to repel tags that would overlap the center card
    var cardRect = null;
    var card = container.querySelector('.profile-center');
    if (card) {
      var cRect = card.getBoundingClientRect();
      var pRect = container.getBoundingClientRect();
      cardRect = {
        left:   cRect.left   - pRect.left   - 8,
        right:  cRect.right  - pRect.left   + 8,
        top:    cRect.top    - pRect.top    - 8,
        bottom: cRect.bottom - pRect.top    + 8,
      };
    }
    function intersectsCard(x, y, w, h) {
      if (!cardRect) return false;
      return !(x + w < cardRect.left || x > cardRect.right
            || y + h < cardRect.top  || y > cardRect.bottom);
    }
    var GAP = 4; // min pixel gap between any two tag pills
    function intersectsAny(x, y, w, h) {
      for (var k = 0; k < placed.length; k++) {
        var r = placed[k];
        if (!(x + w + GAP < r.x || x - GAP > r.x + r.w
           || y + h + GAP < r.y || y - GAP > r.y + r.h)) return true;
      }
      return false;
    }
    function place(tag, angle) {
      // Push outward radially until the tag clears the card AND every other tag
      var rx = radiusX, ry = radiusY, x, y, attempts = 0;
      do {
        x = cx + rx * Math.cos(angle) - tag.offsetWidth / 2;
        y = cy + ry * Math.sin(angle) - tag.offsetHeight / 2;
        var bad = intersectsCard(x, y, tag.offsetWidth, tag.offsetHeight)
               || intersectsAny (x, y, tag.offsetWidth, tag.offsetHeight);
        if (!bad) break;
        rx *= 1.05;
        ry *= 1.04;
        attempts++;
      } while (attempts < 50);
      x = Math.max(4, Math.min(x, maxX - tag.offsetWidth - 4));
      y = Math.max(4, Math.min(y, maxY - tag.offsetHeight - 4));
      tag.style.left = x + 'px';
      tag.style.top = y + 'px';
      placed.push({ x: x, y: y, w: tag.offsetWidth, h: tag.offsetHeight });
    }
    // Distribute around the FULL ellipse — card collision pushes top/bottom
    // tags outward automatically, so we don't need the old "left/right arc only".
    // Start from the right and walk counter-clockwise so the first few tags
    // (most prominent positions) land on the right side.
    for (var i = 0; i < count; i++) {
      var a = (2 * Math.PI * i / count) + (offsetAngle || 0);
      place(tags[i], a);
    }
  }

  function layoutAllOrbits() {
    var w = document.querySelector('.profile-orbit');
    if (!w) return;
    var ww = w.offsetWidth;
    // Inner (experience) = closer ellipse, outer (skills) = wider ellipse
    var innerRx = Math.min(ww * 0.30, 350);
    var innerRy = 160;
    var outerRx = Math.min(ww * 0.44, 540);
    var outerRy = 210;
    var placed = []; // shared so outer tags avoid inner tags
    layoutOrbit('.orbit-inner', innerRx, innerRy, 0,    placed);
    layoutOrbit('.orbit-outer', outerRx, outerRy, 0.05, placed);
    var innerEll = document.querySelector('.orbit-path-inner');
    var outerEll = document.querySelector('.orbit-path-outer');
    if (innerEll) { innerEll.setAttribute('rx', innerRx); innerEll.setAttribute('ry', innerRy); }
    if (outerEll) { outerEll.setAttribute('rx', outerRx); outerEll.setAttribute('ry', outerRy); }
  }

  layoutAllOrbits();
  window.addEventListener('resize', layoutAllOrbits);

  // Randomize orbit-tag colors from a curated palette.
  // Deterministic shuffle (seeded by a hash of the tag text) so colors
  // stay stable across reloads but feel scattered around the orbit.
  var TAG_PALETTE = [
    '52, 211, 153',   // emerald
    '56, 189, 248',   // sky
    '167, 139, 250',  // violet
    '244, 114, 182',  // pink
    '251, 191, 36',   // amber
    '34, 211, 238',   // cyan
    '251, 146, 60',   // orange
    '129, 230, 217',  // mint
    '248, 113, 113',  // rose
  ];
  function hashStr(s) {
    var h = 0;
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    return Math.abs(h);
  }
  function applyTagColors() {
    // Light themes need higher alpha for the pill background to be visible.
    // Fall back to localStorage in case this runs before the theme is restored.
    var theme = document.documentElement.dataset.theme
             || localStorage.getItem('theme')
             || 'dark';
    var isLight = theme === 'light';
    var bgA = isLight ? 0.16 : 0.08;
    var brA = isLight ? 0.45 : 0.28;
    document.querySelectorAll('.orbit-tag').forEach(function (tag, i) {
      var key = (tag.textContent || '').trim() + ':' + i;
      var c = TAG_PALETTE[hashStr(key) % TAG_PALETTE.length];
      tag.style.setProperty('--tag-c',      'rgb('  + c + ')');
      tag.style.setProperty('--tag-bg',     'rgba(' + c + ', ' + bgA + ')');
      tag.style.setProperty('--tag-border', 'rgba(' + c + ', ' + brA + ')');
      tag.style.setProperty('--glow',       'rgba(' + c + ', 0.5)');
      tag.style.setProperty('--glow-outer', 'rgba(' + c + ', 0.15)');
      tag.style.setProperty('--spark',      'rgba(' + c + ', 0.7)');
    });
  }
  applyTagColors();
  // Re-apply when theme changes
  document.querySelectorAll('.theme-dot').forEach(function (d) {
    d.addEventListener('click', function () { setTimeout(applyTagColors, 0); });
  });

  // Tooltip
  var tipBox = document.createElement('div');
  tipBox.className = 'tooltip-box';
  document.body.appendChild(tipBox);

  document.querySelectorAll('[data-tooltip]').forEach(function(el) {
    el.addEventListener('mouseenter', function(e) {
      var text = el.getAttribute('data-tooltip');
      if (!text) return;
      tipBox.textContent = text;
      tipBox.classList.add('visible');
    });
    el.addEventListener('mousemove', function(e) {
      var x = e.clientX + 12;
      var y = e.clientY - 8;
      if (x + tipBox.offsetWidth > window.innerWidth - 8) x = e.clientX - tipBox.offsetWidth - 12;
      if (y < 8) y = e.clientY + 16;
      tipBox.style.left = x + 'px';
      tipBox.style.top = y + 'px';
    });
    el.addEventListener('mouseleave', function() {
      tipBox.classList.remove('visible');
    });
  });

  // Tag click → navigate to panel
  document.querySelectorAll('.orbit-tag[data-link]').forEach(function(tag) {
    tag.style.cursor = 'pointer';
    tag.addEventListener('click', function() {
      var panel = tag.dataset.link;
      if (!panel) return;
      var navLink = document.querySelector('.panel-nav a[data-panel="' + panel + '"]');
      if (navLink) navLink.click();
      // For research tags, also activate the matching tag filter
      if (panel === 'publications') {
        var activeLang = document.querySelector('[data-lang-btn].active');
        var lang = activeLang ? activeLang.dataset.langBtn : 'zh';
        var langEl = tag.querySelector('[data-lang="' + lang + '"]');
        var tagText = langEl ? langEl.textContent.trim() : tag.textContent.trim();
        var filterBtn = document.querySelector('.tag-btn[data-tag="' + tagText + '"]');
        if (filterBtn) filterBtn.click();
      }
    });
  });

  // Theme switching
  var savedTheme = localStorage.getItem('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  document.querySelectorAll('.theme-dot').forEach(function (dot) {
    if (dot.dataset.theme === savedTheme) dot.classList.add('active');
    dot.addEventListener('click', function () {
      var theme = dot.dataset.theme;
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
      document.querySelectorAll('.theme-dot').forEach(function (d) { d.classList.remove('active'); });
      dot.classList.add('active');
    });
  });

  // Shared state for tag filter + older papers toggle
  var activeTag = 'all';
  var olderVisible = false;

  function applyFilters() {
    document.querySelectorAll('.pub-card').forEach(function (item) {
      var tags = item.dataset.tags.split('||');
      var matchesTag = (activeTag === 'all' || tags.indexOf(activeTag) !== -1);
      var yearHeader = item.previousElementSibling;
      while (yearHeader && !yearHeader.classList.contains('pub-year')) {
        yearHeader = yearHeader.previousElementSibling;
      }
      var yearNum = yearHeader ? parseInt(yearHeader.textContent.trim(), 10) : 9999;
      var isOld = yearNum < 2021;
      var showByAge = isOld ? olderVisible : true;
      item.style.display = (matchesTag && showByAge) ? '' : 'none';
    });
    // Hide year headers with no visible papers
    document.querySelectorAll('.pub-year').forEach(function (header) {
      var yearNum = parseInt(header.textContent.trim(), 10);
      var isOld = yearNum < 2021;
      if (isOld && !olderVisible) { header.style.display = 'none'; return; }
      var next = header.nextElementSibling;
      var hasVisible = false;
      while (next && !next.classList.contains('pub-year')) {
        if (next.classList.contains('pub-card') && next.style.display !== 'none') hasVisible = true;
        next = next.nextElementSibling;
      }
      header.style.display = hasVisible ? '' : 'none';
    });
  }

  // Tag filtering
  document.querySelectorAll('.tag-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      activeTag = btn.dataset.tag;
      document.querySelectorAll('.tag-btn').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      applyFilters();
    });
  });

  // Hide older papers by default
  applyFilters();

  var showOlderBtn = document.getElementById('show-older');
  if (showOlderBtn) {
    showOlderBtn.addEventListener('click', function () {
      olderVisible = !olderVisible;
      applyFilters();
      showOlderBtn.textContent = olderVisible ? 'Hide earlier papers \u25be' : 'Show earlier papers (2011-2019) \u25b8';
    });
  }

  // BibTeX copy button
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('bibtex-copy')) {
      var box = e.target.parentElement;
      var clone = box.cloneNode(true);
      var btn = clone.querySelector('.bibtex-copy');
      if (btn) btn.remove();
      var text = clone.textContent.trim();
      navigator.clipboard.writeText(text).then(function() {
        e.target.textContent = 'Copied!';
        setTimeout(function() { e.target.textContent = 'Copy'; }, 1500);
      });
    }
  });

  // Video poster click-to-play
  document.addEventListener('click', function(e) {
    var poster = e.target.closest('.video-poster');
    if (poster) {
      var embed = poster.dataset.embed;
      var iframe = document.createElement('iframe');
      iframe.src = embed;
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('frameborder', '0');
      poster.parentElement.replaceChild(iframe, poster);
    }
  });

  // Mark recent news (within 90 days)
  var now = new Date();
  document.querySelectorAll('.news-date').forEach(function(el) {
    var parts = el.textContent.trim().split('-');
    var newsDate = new Date(parts[0], (parts[1] || 1) - 1);
    var diffDays = (now - newsDate) / (1000 * 60 * 60 * 24);
    if (diffDays < 90) {
      el.insertAdjacentHTML('afterend', '<span class="news-new">NEW</span>');
    }
  });
});
