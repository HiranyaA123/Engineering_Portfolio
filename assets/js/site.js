// Progressive enhancement only. Every page reads and works without this file.
(function () {
  'use strict';

  /* ---------------------------------------------------------- footer year */

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* ------------------------------------------------- active nav section */

  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.site-nav a[href^="#"]')
  );

  if (navLinks.length && 'IntersectionObserver' in window) {
    var targets = navLinks
      .map(function (link) { return document.querySelector(link.getAttribute('href')); })
      .filter(Boolean);

    var navObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (link) {
          link.classList.toggle(
            'is-current',
            link.getAttribute('href') === '#' + entry.target.id
          );
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    targets.forEach(function (target) { navObserver.observe(target); });
  }

  /* --------------------------------------------------- photo callouts */
  // Hover and focus already reveal a note through CSS. Tapping needs a
  // toggle, and only one note should be open at a time.

  var marks = Array.prototype.slice.call(document.querySelectorAll('.mark'));

  function closeMarks(except) {
    marks.forEach(function (mark) {
      if (mark === except) return;
      mark.classList.remove('is-open');
      var b = mark.querySelector('button');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  }

  marks.forEach(function (mark) {
    var button = mark.querySelector('button');
    if (!button) return;
    button.addEventListener('click', function (event) {
      event.stopPropagation();
      var open = mark.classList.toggle('is-open');
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      closeMarks(mark);
    });
  });

  if (marks.length) {
    document.addEventListener('click', function () { closeMarks(null); });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMarks(null);
    });
  }

  /* -------------------------------------------------------- copy buttons */
  // Anything carrying data-copy gets a button beside it. Only built when the
  // clipboard API exists, so a button that cannot copy never ships.

  var copyables = Array.prototype.slice.call(document.querySelectorAll('[data-copy]'));
  if (copyables.length && navigator.clipboard && navigator.clipboard.writeText) {
    var live = document.createElement('div');
    live.className = 'copy-live';
    live.setAttribute('aria-live', 'polite');
    document.body.appendChild(live);

    var icon = '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6">' +
      '<rect x="5" y="5" width="9" height="9" rx="1.5"/><path d="M11 5V3.5A1.5 1.5 0 0 0 9.5 2h-6A1.5 1.5 0 0 0 2 3.5v6A1.5 1.5 0 0 0 3.5 11H5"/></svg>';

    copyables.forEach(function (el) {
      var what = el.dataset.copyLabel || 'link';
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'copy-btn';
      button.setAttribute('aria-label', 'Copy ' + what);
      button.innerHTML = icon + '<span>Copy</span>';
      el.insertAdjacentElement('afterend', button);

      var timer = null;
      button.addEventListener('click', function () {
        navigator.clipboard.writeText(el.dataset.copy).then(function () {
          button.classList.add('is-done');
          button.querySelector('span').textContent = 'Copied';
          live.textContent = 'Copied ' + what + ' to the clipboard.';
          clearTimeout(timer);
          timer = setTimeout(function () {
            button.classList.remove('is-done');
            button.querySelector('span').textContent = 'Copy';
          }, 1800);
        }, function () {
          button.querySelector('span').textContent = 'Select and copy';
          live.textContent = 'Copying failed. Select the text and copy it instead.';
        });
      });
    });
  }

  /* ------------------------------------------------------------ lightbox */
  // Photographs of hardware are worth looking at closely. Needs <dialog>, so
  // the enlarge control stays hidden unless the browser supports it.

  var photos = Array.prototype.slice.call(document.querySelectorAll('.photo img'));
  if (!photos.length) return;
  if (typeof HTMLDialogElement === 'undefined' || !HTMLDialogElement.prototype.showModal) return;

  document.documentElement.classList.add('js-lightbox');

  var dialog = document.createElement('dialog');
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Enlarged photograph');
  dialog.innerHTML =
    '<div class="lightbox-stage"></div>' +
    '<div class="lightbox-bar">' +
      '<p class="lightbox-caption"></p>' +
      '<button type="button" class="lightbox-close">Close (Esc)</button>' +
    '</div>';
  document.body.appendChild(dialog);

  var stage = dialog.querySelector('.lightbox-stage');
  var caption = dialog.querySelector('.lightbox-caption');
  var closeBtn = dialog.querySelector('.lightbox-close');
  var opener = null;

  function open(img) {
    var figure = img.closest('figure');
    var label = figure ? figure.querySelector('figcaption') : null;

    var full = document.createElement('img');
    full.src = img.dataset.full || img.currentSrc || img.src;
    full.alt = img.alt;
    stage.replaceChildren(full);
    if (label) {
      var labelCopy = label.cloneNode(true);
      var copiedZoom = labelCopy.querySelector('.zoom');
      if (copiedZoom) copiedZoom.remove();
      caption.innerHTML = labelCopy.innerHTML;
    } else {
      caption.textContent = '';
    }

    opener = document.activeElement;
    dialog.showModal();
    closeBtn.focus();
  }

  photos.forEach(function (img) {
    var figure = img.closest('figure');
    if (!figure) return;

    var caps = figure.querySelector('figcaption');
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'zoom';
    var what = figure.dataset.label || 'photograph';
    button.innerHTML = 'Enlarge <span aria-hidden="true">&#43;</span>' +
      '<span class="sr-only"> ' + what + '</span>';
    (caps || figure).appendChild(button);

    button.addEventListener('click', function () { open(img); });
    img.addEventListener('click', function () { open(img); });
  });

  function cleanup() {
    stage.replaceChildren();
    if (opener && opener.focus) opener.focus();
    opener = null;
  }

  function close() {
    if (dialog.open) dialog.close();
    cleanup();
  }

  closeBtn.addEventListener('click', close);

  dialog.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    event.preventDefault();
    close();
  });

  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) close();
  });

  dialog.addEventListener('cancel', function () { setTimeout(cleanup, 0); });
  dialog.addEventListener('close', cleanup);
})();
