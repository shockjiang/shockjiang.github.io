document.addEventListener('DOMContentLoaded', function () {
  // Panel toggling
  document.querySelectorAll('.panel-nav a[data-panel]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelectorAll('.panel').forEach(function (p) { p.style.display = 'none'; });
      document.querySelectorAll('.panel-nav a[data-panel]').forEach(function (a) { a.classList.remove('active'); });
      document.getElementById('panel-' + link.dataset.panel).style.display = 'block';
      link.classList.add('active');
      if (link.dataset.panel === 'projects') {
        document.querySelectorAll('#panel-projects iframe[data-src]').forEach(function(iframe) {
          if (!iframe.src) { iframe.src = iframe.dataset.src; iframe.removeAttribute('data-src'); }
        });
      }
    });
  });

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

  // Orbit tag positioning
  function layoutOrbit(selector, radiusX, radiusY, offsetAngle) {
    var container = document.querySelector('.profile-orbit');
    if (!container) return;
    var tags = container.querySelectorAll(selector + ' .orbit-tag');
    var count = tags.length;
    if (!count) return;
    var cx = container.offsetWidth / 2;
    var cy = container.offsetHeight / 2;
    // Get card bounds to avoid top/bottom placement
    var card = container.querySelector('.profile-center');
    var cardTop = 0, cardBottom = 0;
    if (card) {
      var cRect = card.getBoundingClientRect();
      var pRect = container.getBoundingClientRect();
      cardTop = cRect.top - pRect.top - 10;
      cardBottom = cRect.bottom - pRect.top + 10;
    }
    // Distribute tags on the ellipse but only in left/right arcs
    // Left arc: angles from ~0.6pi to ~1.4pi, Right arc: ~-0.4pi to ~0.4pi
    var half = Math.ceil(count / 2);
    var rightCount = half;
    var leftCount = count - half;
    function place(tag, angle) {
      var x = cx + radiusX * Math.cos(angle) - tag.offsetWidth / 2;
      var y = cy + radiusY * Math.sin(angle) - tag.offsetHeight / 2;
      x = Math.max(4, Math.min(x, container.offsetWidth - tag.offsetWidth - 4));
      y = Math.max(4, Math.min(y, container.offsetHeight - tag.offsetHeight - 4));
      tag.style.left = x + 'px';
      tag.style.top = y + 'px';
    }
    // Right arc: spread from -arcSpan to +arcSpan
    var arcSpan = Math.PI * 0.38;
    for (var i = 0; i < rightCount; i++) {
      var a = -arcSpan + (2 * arcSpan * i / Math.max(rightCount - 1, 1)) + (offsetAngle || 0);
      place(tags[i], a);
    }
    // Left arc: spread from pi-arcSpan to pi+arcSpan
    for (var j = 0; j < leftCount; j++) {
      var a = (Math.PI - arcSpan) + (2 * arcSpan * j / Math.max(leftCount - 1, 1)) + (offsetAngle || 0);
      place(tags[rightCount + j], a);
    }
  }

  function layoutAllOrbits() {
    var w = document.querySelector('.profile-orbit');
    if (!w) return;
    var ww = w.offsetWidth;
    // Inner (experience) = closer ellipse, outer (skills) = wider ellipse
    var innerRx = Math.min(ww * 0.32, 270);
    var innerRy = Math.min(170, 160);
    var outerRx = Math.min(ww * 0.46, 420);
    var outerRy = Math.min(220, 210);
    layoutOrbit('.orbit-inner', innerRx, innerRy, 0);
    layoutOrbit('.orbit-outer', outerRx, outerRy, 0.05);
  }

  layoutAllOrbits();
  window.addEventListener('resize', layoutAllOrbits);

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
      var tagText = tag.textContent.trim();
      if (panel === 'publications') {
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

  // Tag filtering
  document.querySelectorAll('.tag-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var tag = btn.dataset.tag;
      document.querySelectorAll('.tag-btn').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');

      var items = document.querySelectorAll('.pub-card');
      items.forEach(function (item) {
        var tags = item.dataset.tags.split('||');
        if (tag === 'all' || tags.indexOf(tag) !== -1) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });

      // Hide year headers with no visible papers
      document.querySelectorAll('.pub-year').forEach(function (header) {
        var next = header.nextElementSibling;
        var hasVisible = false;
        while (next && !next.classList.contains('pub-year')) {
          if (next.classList.contains('pub-card') && next.style.display !== 'none') {
            hasVisible = true;
          }
          next = next.nextElementSibling;
        }
        header.style.display = hasVisible ? '' : 'none';
      });
    });
  });

  // Hide older papers by default (before 2021)
  function setOlderPapersVisibility(show) {
    document.querySelectorAll('.pub-year').forEach(function (header) {
      var yearNum = parseInt(header.textContent.trim(), 10);
      if (yearNum < 2021) {
        header.style.display = show ? '' : 'none';
        var next = header.nextElementSibling;
        while (next && !next.classList.contains('pub-year')) {
          if (next.classList.contains('pub-card')) {
            next.style.display = show ? '' : 'none';
          }
          next = next.nextElementSibling;
        }
      }
    });
  }
  setOlderPapersVisibility(false);

  var showOlderBtn = document.getElementById('show-older');
  if (showOlderBtn) {
    var olderVisible = false;
    showOlderBtn.addEventListener('click', function () {
      olderVisible = !olderVisible;
      setOlderPapersVisibility(olderVisible);
      showOlderBtn.textContent = olderVisible ? 'Hide earlier papers \u25be' : 'Show earlier papers (2011-2019) \u25b8';
    });
  }

  // BibTeX copy button
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('bibtex-copy')) {
      var text = e.target.parentElement.textContent.replace('Copy', '').trim();
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
