/* ============================================================
   PSDR — Global JavaScript
   Theme toggle, counters, reveal-on-scroll, mobile nav
   ============================================================ */

(function () {
  'use strict';

  // ---------- THEME TOGGLE ----------
  const html = document.documentElement;
  const saved = localStorage.getItem('psdr-theme') || 'light';
  html.setAttribute('data-bs-theme', saved);
  updateThemeIcon(saved);

  document.addEventListener('click', (e) => {
    const toggle = e.target.closest('#themeToggle');
    if (!toggle) return;
    e.preventDefault();
    const next = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-bs-theme', next);
    localStorage.setItem('psdr-theme', next);
    updateThemeIcon(next);
  });

  function updateThemeIcon(theme) {
    document.querySelectorAll('#themeToggle i').forEach((icon) => {
      icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
    });
  }

  // ---------- ANIMATED COUNTERS ----------
  function animateCounter(el, target, duration = 1500) {
    const start = 0;
    const startTime = performance.now();
    function tick(now) {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(start + (target - start) * eased).toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString() + (el.dataset.suffix || '');
    }
    requestAnimationFrame(tick);
  }

  // ---------- REVEAL ON SCROLL ----------
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Trigger counters inside this section
        entry.target.querySelectorAll('[data-counter]').forEach((el) => {
          if (!el.dataset.done) {
            el.dataset.done = '1';
            animateCounter(el, parseInt(el.dataset.counter, 10));
          }
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.psdr-fade-in').forEach((el) => observer.observe(el));

    // Auto-dismiss alerts after 6 seconds
    setTimeout(() => {
      document.querySelectorAll('.alert-dismissible').forEach((el) => {
        if (window.bootstrap && bootstrap.Alert) {
          bootstrap.Alert.getOrCreateInstance(el).close();
        }
      });
    }, 6000);

    // Navbar shrink on scroll
    const nav = document.querySelector('.psdr-navbar');
    if (nav) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 20) nav.style.boxShadow = '0 4px 20px rgba(0,0,0,.06)';
        else nav.style.boxShadow = 'none';
      });
    }
  });

  // ---------- SMOOTH SCROLL FOR ANCHOR LINKS ----------
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href');
    if (id.length < 2) return;
    const target = document.querySelector(id);
    if (!target) return;
    e.preventDefault();
    const top = target.getBoundingClientRect().top + window.scrollY - 90;
    window.scrollTo({ top, behavior: 'smooth' });
  });
})();