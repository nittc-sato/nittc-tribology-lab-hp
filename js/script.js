/**
 * Tribology Laboratory — site scripts
 * - Language toggle (data-ja / data-en attributes)
 * - localStorage persistence
 * - Mobile navigation
 */

(function () {
  "use strict";

  var STORAGE_KEY = "tribology-lab-lang";
  var DEFAULT_LANG = "ja";

  function getStoredLang() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored === "ja" || stored === "en") {
        return stored;
      }
    } catch (e) {
      /* localStorage unavailable */
    }
    return DEFAULT_LANG;
  }

  function setStoredLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* ignore */
    }
  }

  /**
   * Elements with data-ja and data-en: swap textContent.
   * Elements with only data-lang="ja"|"en": show/hide by language.
   */
  function applyLanguage(lang) {
    document.documentElement.lang = lang === "en" ? "en" : "ja";

    var bilingual = document.querySelectorAll("[data-ja][data-en]");
    bilingual.forEach(function (el) {
      var text = el.getAttribute(lang === "en" ? "data-en" : "data-ja");
      if (text !== null) {
        el.textContent = text;
      }
    });

    document.querySelectorAll("[data-lang]").forEach(function (el) {
      var elLang = el.getAttribute("data-lang");
      if (elLang === "ja" || elLang === "en") {
        el.hidden = elLang !== lang;
      }
    });

    document.querySelectorAll(".lang-toggle button").forEach(function (btn) {
      var btnLang = btn.getAttribute("data-set-lang");
      btn.setAttribute("aria-pressed", btnLang === lang ? "true" : "false");
    });

    document.querySelectorAll("img[data-alt-ja][data-alt-en]").forEach(function (img) {
      img.alt = img.getAttribute(lang === "en" ? "data-alt-en" : "data-alt-ja") || "";
    });
  }

  function initLanguage() {
    var lang = getStoredLang();
    applyLanguage(lang);

    document.querySelectorAll(".lang-toggle button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var newLang = btn.getAttribute("data-set-lang");
        if (newLang === "ja" || newLang === "en") {
          setStoredLang(newLang);
          applyLanguage(newLang);
        }
      });
    });
  }

  function initGoogleAnalytics() {
    var id = typeof window.TRIBOLOGY_GA4_ID === "string" ? window.TRIBOLOGY_GA4_ID.trim() : "";
    if (!id || !/^G-[A-Z0-9]+$/i.test(id)) {
      return;
    }

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
    window.gtag("js", new Date());
    window.gtag("config", id, { anonymize_ip: true });

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(script);
  }

  function initNavigation() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".main-nav");
    if (!toggle || !nav) return;

    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", expanded ? "false" : "true");
      nav.classList.toggle("is-open", !expanded);
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (window.matchMedia("(max-width: 768px)").matches) {
          toggle.setAttribute("aria-expanded", "false");
          nav.classList.remove("is-open");
        }
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initGoogleAnalytics();
      initLanguage();
      initNavigation();
    });
  } else {
    initGoogleAnalytics();
    initLanguage();
    initNavigation();
  }
})();
