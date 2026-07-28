/* ============================================================
   Velo — Client Logic (Vercel / Linear Optimus Architecture)
   ============================================================ */

(function () {
  "use strict";

  /* ============================================================
     LANDING PAGE — Navbar, Scroll Reveal, Smooth Scroll
     ============================================================ */

  // --- Interactive Global Mouse Spotlight & Grid Texture ---
  var ticking = false;
  window.addEventListener("mousemove", function (e) {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        document.body.style.setProperty("--mouse-x", e.clientX + "px");
        document.body.style.setProperty("--mouse-y", e.clientY + "px");
        if (!document.body.classList.contains("mouse-active")) {
          document.body.classList.add("mouse-active");
        }
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  window.addEventListener("mouseleave", function () {
    document.body.classList.remove("mouse-active");
  });

  // --- Navbar scroll effect ---
  var navbar = document.getElementById("navbar");
  if (navbar) {
    var onScroll = function () {
      if (window.scrollY > 24) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // --- i18n Internationalization Engine ---
  var currentLang = "es";

  function getTranslation(key) {
    if (window.TRANSLATIONS && window.TRANSLATIONS[currentLang] && window.TRANSLATIONS[currentLang][key]) {
      return window.TRANSLATIONS[currentLang][key];
    }
    if (window.TRANSLATIONS && window.TRANSLATIONS["es"] && window.TRANSLATIONS["es"][key]) {
      return window.TRANSLATIONS["es"][key];
    }
    return key;
  }

  function applyLanguage(lang) {
    currentLang = (lang === "en") ? "en" : "es";
    try {
      localStorage.setItem("velo_lang", currentLang);
    } catch (e) {}

    document.documentElement.lang = currentLang;

    var btnLangToggle = document.getElementById("btn-lang-toggle");
    if (btnLangToggle) {
      var optEs = btnLangToggle.querySelector(".lang-es");
      var optEn = btnLangToggle.querySelector(".lang-en");
      if (optEs) optEs.classList.toggle("active", currentLang === "es");
      if (optEn) optEn.classList.toggle("active", currentLang === "en");
    }

    var elements = document.querySelectorAll("[data-i18n]");
    elements.forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var translated = getTranslation(key);
      if (translated) {
        if (translated.includes("<") && translated.includes(">")) {
          el.innerHTML = translated;
        } else {
          el.textContent = translated;
        }
      }
    });

    var phElements = document.querySelectorAll("[data-i18n-ph]");
    phElements.forEach(function (el) {
      var key = el.getAttribute("data-i18n-ph");
      var translated = getTranslation(key);
      if (translated) {
        el.setAttribute("placeholder", translated);
      }
    });

    if (typeof updateExportSummary === "function") {
      updateExportSummary();
    }
  }

  function initLanguage() {
    var saved = null;
    try {
      saved = localStorage.getItem("velo_lang");
    } catch (e) {}

    if (!saved) {
      var navLang = navigator.language || navigator.userLanguage || "es";
      saved = navLang.toLowerCase().startsWith("es") ? "es" : "en";
    }

    applyLanguage(saved);

    var btnLangToggle = document.getElementById("btn-lang-toggle");
    if (btnLangToggle) {
      btnLangToggle.addEventListener("click", function () {
        var nextLang = (currentLang === "es") ? "en" : "es";
        applyLanguage(nextLang);
      });
    }
  }

  // --- PayPal Hosted Donation Button Render ---
  function initPayPalButton() {
    if (window.paypal && typeof window.paypal.HostedButtons === "function") {
      var container = document.getElementById("paypal-container-EW4SNGL8SU6Z2");
      if (container && container.children.length === 0) {
        window.paypal.HostedButtons({
          hostedButtonId: "EW4SNGL8SU6Z2",
        }).render("#paypal-container-EW4SNGL8SU6Z2");
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPayPalButton);
  } else {
    initPayPalButton();
  }

  // --- Smooth scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var target = document.querySelector(link.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // --- Scroll reveal (IntersectionObserver) ---
  var revealElements = document.querySelectorAll(".reveal");
  if (revealElements.length > 0 && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    revealElements.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealElements.forEach(function (el) {
      el.classList.add("visible");
    });
  }


  /* ============================================================
     DOWNLOAD TOOL — Application Logic
     ============================================================ */

  // --- DOM Elements ---
  var urlInput       = document.getElementById("url-input");
  var btnFetch       = document.getElementById("btn-fetch");
  var btnPaste       = document.getElementById("btn-paste");
  var btnClearUrl    = document.getElementById("btn-clear-url");
  var inputError     = document.getElementById("input-error");

  var videoCard      = document.getElementById("video-card");
  var videoThumb     = document.getElementById("video-thumb");
  var videoTitle     = document.getElementById("video-title");
  var videoUploader  = document.getElementById("video-uploader");
  var videoDuration  = document.getElementById("video-duration");

  var formatsSection = document.getElementById("formats-section");
  var formatsBody    = document.getElementById("formats-body");
  var emptyGroup     = document.getElementById("empty-group");
  var btnDownload    = document.getElementById("btn-download");

  var resolutionsGrid    = document.getElementById("resolutions-grid");
  var downloadTypeCards  = document.querySelectorAll(".download-type-card");
  var btnToggleAdvanced  = document.getElementById("btn-toggle-advanced");
  var advancedOptionsPanel = document.getElementById("advanced-options-panel");

  // Summary Card DOM Elements
  var summaryThumb       = document.getElementById("summary-thumb");
  var summaryVideoTitle  = document.getElementById("summary-video-title");
  var summaryVideoUploader = document.getElementById("summary-video-uploader");
  var summaryType        = document.getElementById("summary-type");
  var summaryResolution  = document.getElementById("summary-resolution");
  var summaryFormat      = document.getElementById("summary-format");
  var summaryDuration    = document.getElementById("summary-duration");
  var summarySize        = document.getElementById("summary-size");
  var summaryTools       = document.getElementById("summary-tools");
  var checkUrl           = document.getElementById("check-url");
  var checkQuality       = document.getElementById("check-quality");
  var checkConfig        = document.getElementById("check-config");

  // Optional Tools DOM Elements
  var subtitlesToggle    = document.getElementById("subtitles-toggle");
  var gifToggle          = document.getElementById("gif-toggle");
  var gifControls        = document.getElementById("gif-controls");

  // Trim & Clip DOM Elements
  var trimToggle     = document.getElementById("trim-toggle");
  var trimBadge      = document.getElementById("trim-badge");
  var trimControls   = document.getElementById("trim-controls");
  var trimStartRange = document.getElementById("trim-start-range");
  var trimEndRange   = document.getElementById("trim-end-range");
  var trimStartInput = document.getElementById("trim-start-input");
  var trimEndInput   = document.getElementById("trim-end-input");
  var trimHighlight  = document.getElementById("trim-highlight");
  var presetBtns     = document.querySelectorAll(".preset-btn");

  var progressSection = document.getElementById("progress-section");
  var progressBar     = document.getElementById("progress-bar");
  var progressPct     = document.getElementById("progress-pct");
  var progressLabel   = document.getElementById("progress-label");
  var progressSize    = document.getElementById("progress-size");
  var progressSpeed   = document.getElementById("progress-speed");
  var progressEta     = document.getElementById("progress-eta");

  var statusSection  = document.getElementById("status-section");
  var statusMsg      = document.getElementById("status-msg");

  var toggleWebM     = document.getElementById("toggle-webm");

  // --- State ---
  var currentUrl = "";
  var selectedFormat = null;
  var allGroups = {};
  var activeGroup = "video";
  var pollTimer = null;

  var totalDurationSecs = 0;
  var trimStartSecs = 0;
  var trimEndSecs = 0;

  // --- Helpers ---
  function setLoading(btn, on) {
    if (!btn) return;
    btn.classList.toggle("loading", on);
    btn.disabled = on;
  }

  function showError(msg) { inputError.textContent = msg; }
  function clearError()   { inputError.textContent = ""; }

  function showStatus(msg, type) {
    if (!statusSection || !statusMsg) return;
    statusSection.classList.remove("hidden");
    statusMsg.textContent = msg;
    statusMsg.className = "status-msg " + type;
  }

  function hideStatus() { if (statusSection) statusSection.classList.add("hidden"); }

  function formatBytes(bytes) {
    if (!bytes || bytes <= 0) return "";
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
  }

  function formatSize(val) {
    if (typeof val === "number") return val.toFixed(1) + " MB";
    return val || "\u2014";
  }

  function formatEta(secs) {
    if (!secs || secs <= 0) return "";
    var m = Math.floor(secs / 60);
    var s = Math.floor(secs % 60);
    return m > 0 ? m + "m " + s + "s" : s + "s";
  }

  function esc(str) {
    var d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
  }

  function renderVideoCard(data) {
    if (videoThumb) {
      videoThumb.onerror = function () {
        this.style.display = "none";
      };
      videoThumb.src = data.thumbnail || "";
    }
    if (videoTitle) videoTitle.textContent = data.title || "Sin título";
    if (videoUploader) videoUploader.textContent = data.uploader ? "Por " + data.uploader : "";
    if (videoDuration) videoDuration.textContent = data.duration ? secondsToTimeStr(data.duration) : "";
    if (videoCard) videoCard.classList.remove("hidden");

    if (summaryThumb) {
      summaryThumb.onerror = function () {
        this.src = "/static/favicon.svg";
      };
      summaryThumb.src = data.thumbnail || "/static/favicon.svg";
    }
    if (summaryVideoTitle) summaryVideoTitle.textContent = data.title || "Sin título";
    if (summaryVideoUploader) summaryVideoUploader.textContent = data.uploader ? "Por " + data.uploader : "";
    if (summaryDuration) summaryDuration.textContent = data.duration ? secondsToTimeStr(data.duration) : "--:--";
    updateExportSummary();
  }


  // --- Trim & Clip Logic (CapCut Style) ---
  function secondsToTimeStr(secs) {
    if (isNaN(secs) || secs < 0) secs = 0;
    var h = Math.floor(secs / 3600);
    var m = Math.floor((secs % 3600) / 60);
    var s = Math.floor(secs % 60);
    if (h > 0) {
      return h + ":" + (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }
    return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
  }

  function timeStrToSeconds(str) {
    if (!str) return 0;
    var parts = str.trim().split(":").map(function (p) { return parseFloat(p) || 0; });
    if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2];
    } else if (parts.length === 2) {
      return parts[0] * 60 + parts[1];
    } else if (parts.length === 1) {
      return parts[0];
    }
    return 0;
  }

  function updateTrimUI() {
    if (totalDurationSecs <= 0) return;

    var start = parseFloat(trimStartRange.value) || 0;
    var end = parseFloat(trimEndRange.value) || totalDurationSecs;

    if (start >= end) {
      start = Math.max(0, end - 1);
      trimStartRange.value = start;
    }
    if (end <= start) {
      end = Math.min(totalDurationSecs, start + 1);
      trimEndRange.value = end;
    }

    trimStartSecs = start;
    trimEndSecs = end;

    var pctStart = (start / totalDurationSecs) * 100;
    var pctEnd = (end / totalDurationSecs) * 100;

    trimHighlight.style.left = pctStart + "%";
    trimHighlight.style.width = Math.max(0, pctEnd - pctStart) + "%";

    trimStartInput.value = secondsToTimeStr(start);
    trimEndInput.value = secondsToTimeStr(end);

    var diff = Math.round(end - start);
    trimBadge.textContent = "Clip: " + secondsToTimeStr(start) + " - " + secondsToTimeStr(end) + " (" + diff + "s)";
  }

  if (trimToggle) {
    trimToggle.addEventListener("change", function () {
      var isChecked = trimToggle.checked;
      trimControls.classList.toggle("hidden", !isChecked);
      trimBadge.classList.toggle("hidden", !isChecked);
      if (isChecked) updateTrimUI();
    });
  }

  if (trimStartRange && trimEndRange) {
    trimStartRange.addEventListener("input", updateTrimUI);
    trimEndRange.addEventListener("input", updateTrimUI);
  }

  if (trimStartInput && trimEndInput) {
    trimStartInput.addEventListener("change", function () {
      var parsed = timeStrToSeconds(trimStartInput.value);
      trimStartRange.value = Math.min(parsed, trimEndSecs - 1);
      updateTrimUI();
    });
    trimEndInput.addEventListener("change", function () {
      var parsed = timeStrToSeconds(trimEndInput.value);
      trimEndRange.value = Math.max(parsed, trimStartSecs + 1);
      updateTrimUI();
    });
  }

  presetBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      presetBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");

      var p = btn.dataset.preset;
      if (p === "all") {
        trimStartRange.value = 0;
        trimEndRange.value = totalDurationSecs;
      } else {
        var duration = parseFloat(p) || 15;
        trimStartRange.value = 0;
        trimEndRange.value = Math.min(totalDurationSecs, duration);
      }
      updateTrimUI();
    });
  });

  // --- Fetch info ---
  async function fetchInfo() {
    var url = urlInput.value.trim();
    if (!url) { showError("Por favor ingresa una URL válida."); return; }

    clearError();
    hideStatus();
    videoCard.classList.add("hidden");
    formatsSection.classList.add("hidden");
    progressSection.classList.add("hidden");
    selectedFormat = null;
    btnDownload.disabled = true;
    currentUrl = url;

    setLoading(btnFetch, true);

    try {
      var res = await fetch("/api/info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url }),
      });

      var data = await res.json();

      if (!res.ok) {
        showError(data.error || "Error al obtener la información del contenido.");
        return;
      }

      renderVideoCard(data);

      totalDurationSecs = data.duration || 0;
      if (totalDurationSecs > 0) {
        trimStartRange.max = totalDurationSecs;
        trimEndRange.max = totalDurationSecs;
        trimStartRange.value = 0;
        trimEndRange.value = totalDurationSecs;
        updateTrimUI();
      }

      var rawGroups = data.groups || {};
      var videoList = [];

      if (rawGroups.combined) {
        videoList = videoList.concat(rawGroups.combined);
      }

      if (data.has_ffmpeg && rawGroups.video_only) {
        videoList = videoList.concat(rawGroups.video_only);
      }

      function getResolutionHeight(resStr) {
        if (!resStr) return 0;
        var m = resStr.match(/(\d+)[pP]/);
        if (m) return parseInt(m[1], 10);
        m = resStr.match(/[xX](\d+)/);
        if (m) return parseInt(m[1], 10);
        m = resStr.match(/(\d+)/);
        return m ? parseInt(m[1], 10) : 0;
      }

      videoList.sort(function (a, b) {
        var heightA = getResolutionHeight(a.resolution);
        var heightB = getResolutionHeight(b.resolution);
        if (heightA !== heightB) {
          return heightB - heightA;
        }
        return b.format_id.localeCompare(a.format_id);
      });

      // Master Audio Options
      var audioList = rawGroups.audio_only || [];
      audioList.unshift(
        { format_id: "mp3_320k", resolution: "audio only", ext: "mp3 (320k)", filesize: "Máster HD", category: "audio_only" },
        { format_id: "wav", resolution: "audio only", ext: "wav", filesize: "Sin compresión", category: "audio_only" }
      );

      // Video-only list (separate group for "Solo video" card)
      var videoOnlyList = [];
      if (rawGroups.video_only) {
        videoOnlyList = rawGroups.video_only.slice();
        videoOnlyList.sort(function (a, b) {
          var heightA = getResolutionHeight(a.resolution);
          var heightB = getResolutionHeight(b.resolution);
          if (heightA !== heightB) return heightB - heightA;
          return b.format_id.localeCompare(a.format_id);
        });
      }

      allGroups = {
        video: videoList,
        audio: audioList,
        video_only: videoOnlyList
      };

      // Populate Subtitles dropdown if available
      var subs = data.subtitles || [];
      if (subLangSelect) {
        subLangSelect.innerHTML = "";
        if (subs.length > 0) {
          subs.forEach(function (s) {
            var opt = document.createElement("option");
            opt.value = s.code;
            opt.textContent = s.name;
            subLangSelect.appendChild(opt);
          });
          if (subtitlesSection) subtitlesSection.classList.remove("hidden");
        } else {
          if (subtitlesSection) subtitlesSection.classList.add("hidden");
        }
      }

      if (btnExportGif) {
        btnExportGif.classList.remove("hidden");
      }

      if (allGroups.video && allGroups.video.length > 0) {
        switchTab("video");
      } else if (allGroups.audio && allGroups.audio.length > 0) {
        switchTab("audio");
      } else {
        showError("No se encontraron formatos descargables para esta URL.");
        return;
      }

      formatsSection.classList.remove("hidden");
    } catch (err) {
      console.error("Error en fetchInfo:", err);
      showError(err.message && err.name !== "TypeError" ? err.message : "Error de conexión con el servidor.");
    } finally {
      setLoading(btnFetch, false);
    }
  }
  var deferredPrompt = null;
  var btnPwaInstall = document.getElementById("btn-pwa-install");

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).then(function (reg) {
        console.log("Velo Service Worker registrado:", reg.scope);
      }).catch(function (err) {
        console.warn("Error al registrar Service Worker:", err);
      });
    });
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    deferredPrompt = e;
    if (btnPwaInstall) {
      btnPwaInstall.classList.remove("hidden");
    }
  });

  if (btnPwaInstall) {
    btnPwaInstall.addEventListener("click", function () {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(function (choice) {
        if (choice.outcome === "accepted") {
          console.log("PWA instalada por el usuario.");
        }
        deferredPrompt = null;
        btnPwaInstall.classList.add("hidden");
      });
    });
  }

  // Web Share Target Query Params (?url=...)
  var urlParams = new URLSearchParams(window.location.search);
  var sharedUrl = urlParams.get("url") || urlParams.get("text");
  if (sharedUrl && urlInput) {
    urlInput.value = sharedUrl;
    setTimeout(fetchInfo, 300);
  }

  // Input Mode Tabs (Single vs Batch)
  var modeTabs = document.querySelectorAll(".mode-tab");
  var singleWrap = document.getElementById("single-input-wrap");
  var batchWrap = document.getElementById("batch-input-wrap");

  modeTabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      modeTabs.forEach(function (t) { t.classList.remove("active"); });
      tab.classList.add("active");
      var isBatch = tab.dataset.mode === "batch";
      if (singleWrap) singleWrap.classList.toggle("hidden", isBatch);
      if (batchWrap) batchWrap.classList.toggle("hidden", !isBatch);
    });
  });

  // Batch Download Handler
  var btnBatchFetch = document.getElementById("btn-batch-fetch");
  var batchUrlInput = document.getElementById("batch-url-input");

  if (btnBatchFetch && batchUrlInput) {
    btnBatchFetch.addEventListener("click", async function () {
      var raw = batchUrlInput.value.trim();
      if (!raw) { showError("Por favor ingresa al menos una URL."); return; }
      clearError();
      hideStatus();
      setLoading(btnBatchFetch, true);

      try {
        var res = await fetch("/api/batch/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ urls: raw, format_id: "best" }),
        });
        var data = await res.json();
        if (!res.ok || data.error) {
          showError(data.error || "Error al iniciar descarga en lote.");
          return;
        }
        pollProgress(data.download_id);
      } catch (err) {
        showError("Error de conexión al procesar el lote.");
      } finally {
        setLoading(btnBatchFetch, false);
      }
    });
  }

  // Subtitles DOM Elements
  var subtitlesSection = document.getElementById("subtitles-section");
  var subLangSelect = document.getElementById("sub-lang-select");
  var btnSubSrt = document.getElementById("btn-sub-srt");
  var btnSubVtt = document.getElementById("btn-sub-vtt");
  var btnSubTxt = document.getElementById("btn-sub-txt");
  var btnExportGif = document.getElementById("btn-export-gif");

  function downloadSubtitleFormat(fmt) {
    if (!currentUrl) return;
    var lang = subLangSelect ? subLangSelect.value : "es";
    showStatus("Descargando subtítulos (" + fmt.toUpperCase() + ")...", "info");

    fetch("/api/subtitles/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: currentUrl, lang: lang, fmt: fmt }),
    }).then(function (res) {
      if (!res.ok) throw new Error("No se pudieron descargar los subtítulos.");
      return res.blob();
    }).then(function (blob) {
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "subtitles_" + lang + "." + fmt;
      a.click();
      hideStatus();
    }).catch(function (err) {
      showError(err.message);
    });
  }

  if (btnSubSrt) btnSubSrt.addEventListener("click", function () { downloadSubtitleFormat("srt"); });
  if (btnSubVtt) btnSubVtt.addEventListener("click", function () { downloadSubtitleFormat("vtt"); });
  if (btnSubTxt) btnSubTxt.addEventListener("click", function () { downloadSubtitleFormat("txt"); });

  // GIF Export Handler
  if (btnExportGif) {
    btnExportGif.addEventListener("click", async function () {
      if (!currentUrl) return;
      showStatus("Generando GIF animado con alta paleta de colores...", "info");
      setLoading(btnExportGif, true);

      try {
        var res = await fetch("/api/convert/gif", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            url: currentUrl,
            start_seconds: trimStartSecs,
            end_seconds: trimEndSecs
          }),
        });

        if (!res.ok) {
          var errData = await res.json();
          throw new Error(errData.error || "Error al exportar GIF.");
        }

        var blob = await res.blob();
        var a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "clip_animado.gif";
        a.click();
        hideStatus();
      } catch (err) {
        showError(err.message);
      } finally {
        setLoading(btnExportGif, false);
      }
    });
  }

  // --- Live Summary Update ---
  function updateExportSummary() {
    if (checkUrl) checkUrl.classList.toggle("active", Boolean(currentUrl));

    if (selectedFormat) {
      if (checkQuality) checkQuality.classList.add("active");
      if (checkConfig) checkConfig.classList.add("active");
      if (summaryResolution) summaryResolution.textContent = selectedFormat.resolution || "--";
      if (summaryFormat) summaryFormat.textContent = (selectedFormat.ext || "mp4").toUpperCase();
      if (summarySize) summarySize.textContent = formatSize(selectedFormat.filesize);
    } else {
      if (checkQuality) checkQuality.classList.remove("active");
      if (checkConfig) checkConfig.classList.remove("active");
      if (summaryResolution) summaryResolution.textContent = getTranslation("summary.pending");
      if (summaryFormat) summaryFormat.textContent = "MP4";
      if (summarySize) summarySize.textContent = "-- MB";
    }

    var typeName = getTranslation("app.type_combo_title");
    if (activeGroup === "audio") typeName = getTranslation("app.type_audio_title");
    if (activeGroup === "video_only") typeName = getTranslation("app.type_video_title");
    if (summaryType) summaryType.textContent = typeName;

    var activeTools = [];
    if (subtitlesToggle && subtitlesToggle.checked) activeTools.push(getTranslation("app.subtitles_label"));
    if (trimToggle && trimToggle.checked) activeTools.push(getTranslation("app.trim_label"));
    if (gifToggle && gifToggle.checked) activeTools.push("GIF");
    if (summaryTools) summaryTools.textContent = activeTools.length ? activeTools.join(", ") : getTranslation("summary.none");
  }

  function clearSummary() {
    if (summaryThumb) summaryThumb.src = "/static/favicon.svg";
    if (summaryVideoTitle) summaryVideoTitle.textContent = getTranslation("summary.waiting_link");
    if (summaryVideoUploader) summaryVideoUploader.textContent = getTranslation("summary.inspect_prompt");
    if (summaryDuration) summaryDuration.textContent = "--:--";
    selectedFormat = null;
    updateExportSummary();
  }

  // --- Paste & Clear Handlers ---
  if (btnPaste && urlInput) {
    btnPaste.addEventListener("click", async function () {
      try {
        var text = await navigator.clipboard.readText();
        if (text) {
          urlInput.value = text.trim();
          fetchInfo();
        }
      } catch (err) {
        console.warn("Clipboard read not allowed:", err);
        showError("No se pudo acceder al portapapeles. Por favor pega el enlace manualmente.");
      }
    });
  }

  if (btnClearUrl) {
    btnClearUrl.addEventListener("click", function () {
      if (urlInput) urlInput.value = "";
      currentUrl = "";
      if (videoCard) videoCard.classList.add("hidden");
      if (formatsSection) formatsSection.classList.add("hidden");
      clearSummary();
    });
  }

  // --- Download Type Selector Cards ---
  downloadTypeCards.forEach(function (card) {
    card.addEventListener("click", function () {
      var group = card.dataset.group || "video";
      switchTab(group);
    });
  });

  // --- Advanced Options Toggle ---
  if (btnToggleAdvanced && advancedOptionsPanel) {
    btnToggleAdvanced.addEventListener("click", function () {
      var isHidden = advancedOptionsPanel.classList.toggle("hidden");
      var span = btnToggleAdvanced.querySelector("span");
      if (span) span.textContent = isHidden ? "Mostrar opciones avanzadas" : "Ocultar opciones avanzadas";
      var chevron = btnToggleAdvanced.querySelector(".chevron-icon");
      if (chevron) chevron.style.transform = isHidden ? "rotate(0deg)" : "rotate(180deg)";
    });
  }

  // --- Tab Switching for Formats ---
  function switchTab(groupName) {
    activeGroup = groupName || "video";

    downloadTypeCards.forEach(function (card) {
      var isTarget = card.dataset.group === activeGroup;
      card.classList.toggle("active", isTarget);
      card.setAttribute("aria-checked", isTarget ? "true" : "false");
    });

    selectedFormat = null;
    if (btnDownload) btnDownload.disabled = true;
    renderFormats(allGroups[activeGroup] || []);
    updateExportSummary();
  }

  if (toggleWebM) {
    toggleWebM.addEventListener("change", function () {
      renderFormats(allGroups[activeGroup] || []);
    });
  }

  // --- Format Grid & Table Rendering ---
  function renderFormats(formats) {
    if (formatsBody) formatsBody.innerHTML = "";
    if (resolutionsGrid) resolutionsGrid.innerHTML = "";

    if (!formats || !formats.length) {
      if (emptyGroup) emptyGroup.classList.remove("hidden");
      if (resolutionsGrid) {
        resolutionsGrid.innerHTML = '<div class="res-card-placeholder">No hay formatos disponibles en esta categoría.</div>';
      }
      return;
    }

    var showWebM = toggleWebM && toggleWebM.checked;
    var filteredFormats = formats;

    if (!showWebM) {
      var resolutionsWithMp4 = {};
      formats.forEach(function (fmt) {
        if (fmt.ext === "mp4") {
          resolutionsWithMp4[fmt.resolution] = true;
        }
      });

      filteredFormats = formats.filter(function (fmt) {
        if (fmt.ext === "webm" && resolutionsWithMp4[fmt.resolution]) {
          return false;
        }
        return true;
      });
    }

    if (!filteredFormats.length) {
      filteredFormats = formats;
    }

    if (emptyGroup) emptyGroup.classList.add("hidden");

    var isRecommendedAssigned = false;

    filteredFormats.forEach(function (fmt, index) {
      // Table Row
      var tr = document.createElement("tr");
      tr.dataset.formatId = fmt.format_id;
      tr.dataset.ext = fmt.ext;

      var resText = esc(fmt.resolution);
      if (fmt.fps && fmt.fps > 30) resText += " " + fmt.fps + "fps";

      tr.innerHTML =
        '<td class="col-radio"><span class="radio-dot"></span></td>' +
        '<td><span class="res-label">' + resText + '</span></td>' +
        '<td>' + esc(fmt.ext) + '</td>' +
        '<td class="col-size">' + esc(formatSize(fmt.filesize)) + '</td>';

      // Grid Resolution Card
      var resCard = document.createElement("div");
      resCard.className = "res-card";
      resCard.dataset.formatId = fmt.format_id;

      var isRec = (!isRecommendedAssigned && (fmt.resolution.includes("1080") || index === 0));
      if (isRec) isRecommendedAssigned = true;

      resCard.innerHTML =
        (isRec ? '<span class="res-card-badge">Recomendado</span>' : '') +
        '<span class="res-card-label">' + esc(fmt.resolution) + '</span>' +
        '<span class="res-card-meta">' + esc(fmt.ext.toUpperCase()) + ' • ' + esc(formatSize(fmt.filesize)) + '</span>';

      var onClick = function () { selectFormat(fmt, tr, resCard); };
      tr.addEventListener("click", onClick);
      resCard.addEventListener("click", onClick);

      if (formatsBody) formatsBody.appendChild(tr);
      if (resolutionsGrid) resolutionsGrid.appendChild(resCard);
    });

    if (filteredFormats.length > 0) {
      var firstTr = formatsBody ? formatsBody.querySelector("tr") : null;
      var firstCard = resolutionsGrid ? resolutionsGrid.querySelector(".res-card") : null;
      selectFormat(filteredFormats[0], firstTr, firstCard);
    }
  }

  function selectFormat(fmt, tr, resCard) {
    if (formatsBody) {
      var prevTr = formatsBody.querySelector("tr.selected");
      if (prevTr) prevTr.classList.remove("selected");
    }
    if (tr) tr.classList.add("selected");

    if (resolutionsGrid) {
      var prevCard = resolutionsGrid.querySelector(".res-card.active");
      if (prevCard) prevCard.classList.remove("active");
    }
    if (resCard) resCard.classList.add("active");

    selectedFormat = {
      format_id: fmt.format_id,
      ext: fmt.ext,
      resolution: fmt.resolution,
      filesize: fmt.filesize,
      category: fmt.category
    };
    if (btnDownload) btnDownload.disabled = false;
    updateExportSummary();
  }

  // --- Download (Async API polling) ---
  async function startDownload() {
    if (!selectedFormat || !currentUrl) return;

    hideStatus();
    progressSection.classList.remove("hidden");
    progressBar.style.width = "0%";
    progressPct.textContent = "0%";
    progressLabel.textContent = "Iniciando descarga...";
    progressSize.textContent = "";
    progressSpeed.textContent = "";
    progressEta.textContent = "";
    setLoading(btnDownload, true);

    try {
      var payload = {
        url: currentUrl,
        format_id: selectedFormat.format_id,
        format_category: selectedFormat.category || "",
      };

      if (trimToggle && trimToggle.checked) {
        payload.start_seconds = trimStartSecs;
        payload.end_seconds = trimEndSecs;
      }

      var res = await fetch("/api/download/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      var data = await res.json();

      if (!res.ok) {
        showStatus(data.error || "Error al iniciar la descarga.", "error");
        progressSection.classList.add("hidden");
        setLoading(btnDownload, false);
        return;
      }

      pollProgress(data.download_id);
    } catch (err) {
      showStatus("Error de conexión.", "error");
      progressSection.classList.add("hidden");
      setLoading(btnDownload, false);
    }
  }

  function pollProgress(downloadId) {
    if (pollTimer) clearInterval(pollTimer);

    pollTimer = setInterval(async function () {
      try {
        var res = await fetch("/api/download/status/" + downloadId);
        var d = await res.json();

        if (!res.ok || (d.status !== "downloading" && d.status !== "done" && d.status !== "error")) {
          clearInterval(pollTimer);
          pollTimer = null;
          progressSection.classList.add("hidden");
          showStatus(d.error || "Se perdió el estado de la descarga. Intenta nuevamente.", "error");
          setLoading(btnDownload, false);
          return;
        }

        if (d.status === "downloading") {
          var pct = d.percent || 0;
          progressBar.style.width = pct + "%";
          progressPct.textContent = pct.toFixed(1) + "%";
          progressLabel.textContent = "Descargando...";

          progressSize.textContent = d.total_bytes > 0
            ? formatBytes(d.downloaded_bytes) + " / " + formatBytes(d.total_bytes)
            : "";
          progressSpeed.textContent = d.speed > 0
            ? formatBytes(d.speed) + "/s"
            : "";
          progressEta.textContent = d.eta > 0
            ? "ETA " + formatEta(d.eta)
            : "";
        }

        if (d.status === "done") {
          clearInterval(pollTimer);
          pollTimer = null;
          progressBar.style.width = "100%";
          progressPct.textContent = "100%";
          progressLabel.textContent = "Completado";
          progressSpeed.textContent = "";
          progressEta.textContent = "";

          var a = document.createElement("a");
          a.href = "/api/download/file/" + downloadId;
          a.download = "";
          document.body.appendChild(a);
          a.click();
          a.remove();

          showStatus("Descarga completada con éxito.", "success");
          setLoading(btnDownload, false);
        }

        if (d.status === "error") {
          clearInterval(pollTimer);
          pollTimer = null;
          progressSection.classList.add("hidden");
          showStatus(d.error || "Error durante el procesamiento.", "error");
          setLoading(btnDownload, false);
        }
      } catch (err) {
        clearInterval(pollTimer);
        pollTimer = null;
        progressSection.classList.add("hidden");
        showStatus("Error de conexión al consultar el estado.", "error");
        setLoading(btnDownload, false);
      }
    }, 500);
  }

  // --- Events ---
  initLanguage();
  btnFetch.addEventListener("click", fetchInfo);
  btnDownload.addEventListener("click", startDownload);
  urlInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") { e.preventDefault(); fetchInfo(); }
  });

})();
