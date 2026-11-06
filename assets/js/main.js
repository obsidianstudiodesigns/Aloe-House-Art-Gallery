(function () {
  'use strict';

  /* Header turns solid once you leave the top of the page. */
  var head = document.querySelector('.site-head');
  var sentinel = document.querySelector('.top-sentinel');
  if (head && sentinel && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      head.classList.toggle('is-solid', !entries[0].isIntersecting);
    }).observe(sentinel);
  }

  /* Viewing room */
  var room = document.getElementById('room');
  var dataEl = document.getElementById('works');
  if (room && dataEl) {
    var works = JSON.parse(dataEl.textContent);
    var img = document.getElementById('room-img');
    var frame = document.getElementById('room-frame');
    var labelEl = document.getElementById('room-label');
    var current = 0;
    var opener = null;
    var list = works;

    var esc = function (s) {
      var d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    };

    var whatsapp = function (w) {
      var text = w.sample
        ? 'Hello Aloe House, I would like to know more about your opening collection.'
        : 'Hello Aloe House, I would like to know more about "' + w.title + '" by ' + w.artist + '.';
      return window.AH.wa + '?text=' + encodeURIComponent(text);
    };

    var show = function (i) {
      current = (i + list.length) % list.length;
      var w = list[current];
      frame.className = 'frame f-' + w.frame;
      frame.style.setProperty('--ar', w.ratio);
      img.removeAttribute('srcset');
      img.src = w.src;
      img.srcset = w.srcset;
      img.sizes = '(max-width: 1023px) 92vw, 62vw';
      img.alt = w.alt;
      var year = w.year ? ', ' + esc(w.year) : '';
      labelEl.innerHTML =
        (w.sample
          ? '<p class="label__sample">Sample artwork</p>'
          : '<p class="label__by">' + esc(w.artist) + '</p>') +
        '<h2 class="label__title">' + esc(w.title) + year + '</h2>' +
        '<p class="label__medium">' + esc(w.medium) + '</p>' +
        (w.sample
          ? '<p class="room__note">This placeholder shows how the collection will be presented. It is not by the gallery’s artists and is not for sale.</p>'
          : '<p class="room__note">Price on request. Ask us about availability, or arrange to see it in person.</p>') +
        '<a class="btn btn--ink" href="' + whatsapp(w) + '" target="_blank" rel="noopener">' +
        (w.sample ? 'Ask about the collection' : 'Enquire about this work') + '</a>';
      try {
        history.replaceState(null, '', '#' + w.slug);
      } catch (err) { /* file:// or sandboxed preview */ }
    };

    var visibleWorks = function () {
      var hidden = {};
      document.querySelectorAll('.piece[hidden] [data-work]').forEach(function (b) {
        hidden[b.dataset.work] = true;
      });
      return works.filter(function (w) { return !hidden[w.slug]; });
    };

    var open = function (slug, from) {
      list = visibleWorks();
      var i = list.findIndex(function (w) { return w.slug === slug; });
      if (i < 0) { list = works; i = list.findIndex(function (w) { return w.slug === slug; }); }
      if (i < 0) return;
      opener = from || null;
      show(i);
      if (!room.open) room.showModal();
    };

    document.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-work]');
      if (b) open(b.dataset.work, b);
    });

    room.addEventListener('close', function () {
      try {
        history.replaceState(null, '', location.pathname + location.search);
      } catch (err) { /* ignore */ }
      if (opener && opener.focus) opener.focus({ preventScroll: true });
    });
    room.querySelector('[data-close]').addEventListener('click', function () { room.close(); });
    room.querySelector('[data-prev]').addEventListener('click', function () { show(current - 1); });
    room.querySelector('[data-next]').addEventListener('click', function () { show(current + 1); });
    room.addEventListener('click', function (ev) {
      if (ev.target === room || ev.target.classList.contains('room__art')) room.close();
    });
    room.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowLeft') show(current - 1);
      if (ev.key === 'ArrowRight') show(current + 1);
    });

    /* Swipe between works on a phone */
    var startX = null;
    room.addEventListener('pointerdown', function (ev) {
      if (ev.pointerType !== 'mouse') startX = ev.clientX;
    });
    room.addEventListener('pointerup', function (ev) {
      if (startX === null) return;
      var dx = ev.clientX - startX;
      startX = null;
      if (Math.abs(dx) > 60) show(current + (dx < 0 ? 1 : -1));
    });

    room.querySelectorAll('[data-wall]').forEach(function (b) {
      b.addEventListener('click', function () {
        room.dataset.wallColour = b.dataset.wall;
        room.querySelectorAll('[data-wall]').forEach(function (o) {
          o.setAttribute('aria-pressed', String(o === b));
        });
      });
    });

    if (location.hash.length > 1) {
      var slug = decodeURIComponent(location.hash.slice(1));
      if (works.some(function (w) { return w.slug === slug; })) open(slug);
    }
  }

  /* While the wall is pinned, keep a focused work in view for keyboard users. */
  var walk = document.querySelector('.walk');
  if (walk) {
    /* Works outside the clipped wall never count as "near the viewport", so load them as the wall approaches. */
    if ('IntersectionObserver' in window) {
      var wallLoader = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        walk.querySelectorAll('img[loading="lazy"]').forEach(function (i) { i.loading = 'eager'; });
        wallLoader.disconnect();
      }, { rootMargin: '120% 0px' });
      wallLoader.observe(walk);
    }
    walk.addEventListener('focusin', function (ev) {
      if (getComputedStyle(walk.querySelector('.walk__view')).position !== 'sticky') return;
      var track = walk.querySelector('.walk__track');
      var item = ev.target.closest('.hang') || ev.target.closest('.walk__end');
      if (!item) return;
      var travel = track.scrollWidth - innerWidth;
      var x = item.offsetLeft + item.offsetWidth / 2 - innerWidth / 2;
      var p = Math.max(0, Math.min(1, x / travel));
      var top = walk.getBoundingClientRect().top + scrollY;
      scrollTo({ top: top + p * (walk.offsetHeight - innerHeight), behavior: 'auto' });
    });
  }

  /* Collection filters */
  var salon = document.getElementById('salon');
  if (salon) {
    var pieces = Array.prototype.slice.call(salon.querySelectorAll('.piece'));
    var empty = document.getElementById('salon-empty');
    var chips = document.querySelectorAll('.chip');
    var apply = function (f) {
      var n = 0;
      pieces.forEach(function (p) {
        var on = f === 'all' || p.dataset.kind === f;
        p.hidden = !on;
        if (on) n++;
      });
      empty.hidden = n > 0;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.filter === f)); });
    };
    document.addEventListener('click', function (ev) {
      var c = ev.target.closest('[data-filter]');
      if (c) apply(c.dataset.filter);
    });
  }

  /* Enquiry form: compose a WhatsApp message on the visitor's own device. */
  var form = document.getElementById('enquiry');
  if (form) {
    var check = function (input) {
      var err = document.getElementById(input.id + '-err');
      var ok = input.value.trim().length > 0;
      err.hidden = ok;
      input.setAttribute('aria-invalid', String(!ok));
      return ok;
    };
    var fName = form.elements.name;
    var fMsg = form.elements.message;
    [fName, fMsg].forEach(function (i) {
      i.addEventListener('blur', function () { if (i.getAttribute('aria-invalid') === 'true') check(i); });
      i.addEventListener('input', function () { if (i.getAttribute('aria-invalid') === 'true') check(i); });
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var a = check(fName);
      var b = check(fMsg);
      if (!a || !b) {
        (a ? fMsg : fName).focus();
        return;
      }
      var text = 'Hello Aloe House, this is ' + fName.value.trim() + '.\nAbout: ' + form.elements.about.value + '\n\n' + fMsg.value.trim();
      window.open('https://wa.me/27837982734?text=' + encodeURIComponent(text), '_blank', 'noopener');
    });
  }
})();
