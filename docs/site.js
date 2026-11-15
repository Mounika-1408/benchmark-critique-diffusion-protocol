(() => {
  "use strict";

  const navLinks = Array.from(document.querySelectorAll(".section-nav a[href^='#']"));
  const sections = navLinks
    .map((link) => document.getElementById(link.getAttribute("href").slice(1)))
    .filter(Boolean);

  let currentId = null;

  function setCurrent(id) {
    if (!id || id === currentId) return;
    currentId = id;
    let activeLink = null;
    navLinks.forEach((link) => {
      if (link.getAttribute("href") === `#${id}`) {
        link.setAttribute("aria-current", "location");
        activeLink = link;
      } else {
        link.removeAttribute("aria-current");
      }
    });

    if (activeLink) {
      const scroller = activeLink.closest(".nav-inner");
      if (scroller && scroller.scrollWidth > scroller.clientWidth + 1) {
        const linkRect = activeLink.getBoundingClientRect();
        const scrollerRect = scroller.getBoundingClientRect();
        if (linkRect.left < scrollerRect.left || linkRect.right > scrollerRect.right) {
          const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          scroller.scrollBy({
            left: linkRect.left - scrollerRect.left - 12,
            behavior: reduceMotion ? "auto" : "smooth",
          });
        }
      }
    }
  }

  function updateCurrentSection() {
    if (!sections.length) return;
    const offset = 90;
    let active = sections[0].id;

    for (const section of sections) {
      if (section.getBoundingClientRect().top <= offset) {
        active = section.id;
      }
    }

    const atBottom =
      window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    if (atBottom) {
      active = sections[sections.length - 1].id;
    }

    setCurrent(active);
  }

  if (sections.length) {
    let ticking = false;
    const requestUpdate = () => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(() => {
        updateCurrentSection();
        ticking = false;
      });
    };

    updateCurrentSection();
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate, { passive: true });
    window.addEventListener("hashchange", updateCurrentSection);
  }

  // Web fonts can change the page height after the browser resolves a URL
  // fragment. Re-align once fonts are ready so direct section links land cleanly.
  function alignHash() {
    if (!window.location.hash) return;
    const id = decodeURIComponent(window.location.hash.slice(1));
    const target = document.getElementById(id);
    if (!target) return;
    const offset = window.innerWidth < 760 ? 54 : 58;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    const root = document.documentElement;
    const previousBehavior = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, Math.max(0, top));
    root.style.scrollBehavior = previousBehavior;
    updateCurrentSection();
  }

  window.addEventListener("load", () => window.requestAnimationFrame(alignHash));

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => window.requestAnimationFrame(alignHash));
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.top = "-1000px";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    const copied = document.execCommand("copy");
    area.remove();
    if (!copied) throw new Error("Copy command was rejected");
  }

  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    const target = document.getElementById(button.getAttribute("data-copy-target"));
    if (!target) return;

    const status = button
      .closest(".code-head")
      ?.querySelector("[data-copy-status]");
    const defaultLabel = button.textContent.trim();
    let resetTimer = null;

    button.addEventListener("click", async () => {
      try {
        await copyText(target.textContent);
        button.textContent = "Copied";
        if (status) status.textContent = "Copied to clipboard.";
      } catch (error) {
        button.textContent = "Copy failed";
        if (status) status.textContent = "Select the text and copy it manually.";
      }

      window.clearTimeout(resetTimer);
      resetTimer = window.setTimeout(() => {
        button.textContent = defaultLabel;
        if (status) status.textContent = "";
      }, 2400);
    });
  });
})();
