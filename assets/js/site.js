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

  // The image element is built on open, so the page never carries an <img>
  // with no source.
  var stage = dialog.querySelector('.lightbox-stage');
  var caption = dialog.querySelector('.lightbox-caption');
  var closeBtn = dialog.querySelector('.lightbox-close');
  var opener = null;

  function open(img) {
    var figure = img.closest('figure');
    var label = figure ? figure.querySelector('figcaption') : null;

    // Skip srcset in the lightbox: it is always the widest file we have.
    var full = document.createElement('img');
    full.src = img.dataset.full || img.currentSrc || img.src;
    full.alt = img.alt;
    stage.replaceChildren(full);
    caption.innerHTML = label ? label.innerHTML : '';

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

    // The button is the keyboard path. Clicking the image itself is a
    // convenience for pointer users on top of it, not instead of it.
    button.addEventListener('click', function () { open(img); });
    img.addEventListener('click', function () { open(img); });
  });

  // Cleanup is driven explicitly rather than from the dialog 'close' event,
  // which does not fire reliably everywhere. Safe to run more than once.
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

  // Click the backdrop (anywhere that is not the image or the bar) to close.
  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) close();
  });

  // Esc dismisses the dialog natively; catch it so focus still comes back.
  dialog.addEventListener('cancel', function () { setTimeout(cleanup, 0); });
  dialog.addEventListener('close', cleanup);
})();
