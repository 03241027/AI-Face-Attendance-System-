'use strict';

function setMode(mode) {
  const body = document.body;
  const btnDark = document.getElementById('btn-dark');
  const btnLight = document.getElementById('btn-light');

  if (mode === 'light') {
    body.classList.remove('dark-mode');
    body.classList.add('light-mode');
    if (btnDark) btnDark.classList.remove('active');
    if (btnLight) btnLight.classList.add('active');
  } else {
    body.classList.remove('light-mode');
    body.classList.add('dark-mode');
    if (btnDark) btnDark.classList.add('active');
    if (btnLight) btnLight.classList.remove('active');
  }

  localStorage.setItem('attendai-theme', mode);
}

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('open');
}

document.addEventListener('click', function (event) {
  const sidebar = document.getElementById('sidebar');
  const hamburger = document.getElementById('hamburger');

  if (!sidebar || !hamburger) return;

  if (
    window.innerWidth <= 1024 &&
    sidebar.classList.contains('open') &&
    !sidebar.contains(event.target) &&
    !hamburger.contains(event.target)
  ) {
    sidebar.classList.remove('open');
  }
});

  document.addEventListener('keydown', function (event) {
    if (event.altKey && !event.shiftKey && !event.ctrlKey && !event.metaKey) {
      const active = document.activeElement;
      if (active && ['INPUT', 'TEXTAREA', 'SELECT'].includes(active.tagName)) {
        return;
      }

      switch (event.key.toLowerCase()) {
        case 'd':
          window.location.href = '/dashboard';
          break;
        case 'a':
          window.location.href = '/mark_attendance';
          break;
        case 'r':
          window.location.href = '/records';
          break;
        case 'f':
          window.location.href = '/test_recognition';
          break;
        default:
          return;
      }
      event.preventDefault();
    }
  });

function animateProgressBars() {
  document.querySelectorAll('.prog-fill').forEach((bar) => {
    const width = bar.dataset.width || bar.style.width;
    bar.style.width = '0';
    setTimeout(() => {
      bar.style.width = width;
    }, 150);
  });
}

function animateCounter(element, target, duration = 900) {
  if (!element) return;
  
  const start = 0;
  const startTime = Date.now();
  const suffix = element.dataset.suffix || '';
  
  const animate = () => {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const current = Math.floor(start + (target - start) * progress);
    element.textContent = `${current}${suffix}`;
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      element.textContent = `${target}${suffix}`;
    }
  };
  
  animate();
}

function updateClock() {
  const sub = document.querySelector('.page-sub');
  if (!sub) return;
  const now = new Date();
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const dateStr = now.toLocaleDateString('en-GB', options);
  const timeStr = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
  if (document.getElementById('page-dashboard')) {
    sub.innerHTML = `<span class="live-dot" aria-hidden="true"></span> Live monitoring — ${dateStr}, ${timeStr}`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('attendai-theme');
  if (saved === 'light') {
    setMode('light');
  }

  document.querySelectorAll('.stat-row .stat-val').forEach((el) => {
    const text = el.textContent.trim();
    const match = text.match(/^(\d+)(%)?$/);
    if (!match) return;

    el.dataset.suffix = match[2] || '';
    animateCounter(el, Number(match[1]), 700);
  });

  animateProgressBars();
  updateClock();
  setInterval(updateClock, 30000);
});
