document.addEventListener('DOMContentLoaded', function () {
  // Panel toggling
  document.querySelectorAll('.panel-nav a[data-panel]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelectorAll('.panel').forEach(function (p) { p.style.display = 'none'; });
      document.querySelectorAll('.panel-nav a[data-panel]').forEach(function (a) { a.classList.remove('active'); });
      document.getElementById('panel-' + link.dataset.panel).style.display = 'block';
      link.classList.add('active');
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
    tags.forEach(function(tag, i) {
      var angle = (2 * Math.PI * i / count) + (offsetAngle || 0);
      var x = cx + radiusX * Math.cos(angle) - tag.offsetWidth / 2;
      var y = cy + radiusY * Math.sin(angle) - tag.offsetHeight / 2;
      tag.style.left = x + 'px';
      tag.style.top = y + 'px';
    });
  }

  function layoutAllOrbits() {
    var w = document.querySelector('.profile-orbit');
    if (!w) return;
    var ww = w.offsetWidth;
    var innerRx = Math.min(ww * 0.32, 260);
    var innerRy = Math.min(160, 140);
    var outerRx = Math.min(ww * 0.46, 400);
    var outerRy = Math.min(200, 185);
    layoutOrbit('.orbit-inner', innerRx, innerRy, -0.3);
    layoutOrbit('.orbit-outer', outerRx, outerRy, 0.15);
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

      var items = document.querySelectorAll('.pub-item');
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
          if (next.classList.contains('pub-item') && next.style.display !== 'none') {
            hasVisible = true;
          }
          next = next.nextElementSibling;
        }
        header.style.display = hasVisible ? '' : 'none';
      });
    });
  });
});
