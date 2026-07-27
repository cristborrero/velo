/* ============================================================
   VELO MULTILINGUAL DICTIONARY (ES / EN)
   ============================================================ */
var TRANSLATIONS = {
  es: {
    // Navbar
    "nav.features": "Funciones",
    "nav.process": "Proceso",
    "nav.faq": "FAQ",
    "nav.donate": "Donar",
    "nav.cta": "Usar Velo",

    // Hero
    "hero.badge_tag": "Velo v2.0",
    "hero.badge_text": "Nueva arquitectura SaaS: Descargas masivas .ZIP, Recorte CapCut y Audio HD",
    "hero.title_1": "Descarga y procesa medios",
    "hero.title_2": "en calidad original.",
    "hero.subtitle": "Una suite multimedia completa de alto rendimiento. Inspecciona resoluciones 4K, recorta fragmentos en tiempo real, extrae audio en alta fidelidad y descarga playlists completas en archivos .ZIP.",
    "hero.btn_app": "Abrir Velo App",
    "hero.btn_features": "Ver capacidades v2.0",
    "hero.platforms": "Compatibilidad nativa con YouTube, TikTok, Instagram, Twitter/X, Vimeo, Twitch y +1000 plataformas",

    // App Section
    "app.title": "Velo App — Downloader & Processor",
    "app.mode_single": "URL única",
    "app.mode_batch": "Lista / Playlist (.ZIP)",
    "app.mode_local": "Archivo local",
    "app.url_placeholder": "Pega el enlace de video, audio o playlist aquí...",
    "app.paste": "Pegar",
    "app.inspect": "Inspeccionar",
    "app.batch_placeholder": "Pega múltiples URLs (una por línea)...",
    "app.batch_btn": "Procesar Lista (.ZIP)",
    "app.local_drop": "Arrastra un archivo de video/audio aquí o haz clic para seleccionar",
    "app.detected_badge": "Contenido detectado",

    // Download Types
    "app.type_title": "2. Elige qué quieres obtener",
    "app.type_combo_title": "Video + audio",
    "app.type_combo_desc": "Contenido completo en calidad HD / 4K",
    "app.type_audio_title": "Solo audio",
    "app.type_audio_desc": "Extrae pistas de música o podcast (MP3/WAV)",
    "app.type_video_title": "Solo video",
    "app.type_video_desc": "Flujo de video sin pista sonora",
    "app.webm_compatibility": "Compatibilidad WebM",

    // Resolutions & Formats
    "app.formats_title": "3. Calidad disponible",
    "app.empty_formats": "No se encontraron formatos descargables para esta categoría.",

    // Advanced Options
    "app.toggle_advanced": "Mostrar opciones avanzadas",
    "app.toggle_advanced_hide": "Ocultar opciones avanzadas",
    "app.subtitles_label": "Extraer Subtítulos",
    "app.subtitles_lang": "Idioma de subtítulos:",
    "app.trim_label": "Recortar Clip (CapCut Trim)",
    "app.gif_label": "Convertir a GIF Animado",
    "app.gif_btn": "Exportar como GIF",

    // Summary Card
    "summary.title": "Resumen de exportación",
    "summary.waiting_link": "Esperando enlace...",
    "summary.inspect_prompt": "Inspecciona una URL",
    "summary.type": "Tipo de descarga:",
    "summary.quality": "Calidad elegida:",
    "summary.format": "Formato final:",
    "summary.size": "Tamaño estimado:",
    "summary.tools": "Herramientas activas:",
    "summary.checklist_title": "Lista de comprobación antes de procesar",
    "summary.check_url": "URL verificada",
    "summary.check_quality": "Calidad seleccionada",
    "summary.check_config": "Configuración completa",
    "summary.btn_download": "Iniciar descarga",
    "summary.microcopy": "Podrás revisar el nombre y la ubicación del archivo antes de guardarlo.",
    "summary.pending": "Por seleccionar",
    "summary.none": "Ninguna",

    // Bento Grid Features
    "features.badge": "Capacidades v2.0",
    "features.main_title": "Diseñado para máxima velocidad.<br>Sin intermediarios.",
    "features.main_sub": "Arquitectura asíncrona de alto rendimiento optimizada para la web moderna.",
    "features.card1_title": "Interfaz SaaS de 2 Columnas con Resumen Sticky",
    "features.card1_desc": "Organización en dos columnas optimizadas: panel de control de opciones a la izquierda y resumen lateral flotante a la derecha con validación automática antes de procesar.",
    "features.card2_title": "Descargas Masivas (.ZIP)",
    "features.card2_desc": "Descarga listas de reproducción y múltiples enlaces procesados en lote, empaquetados en un único archivo comprimido .ZIP.",
    "features.card3_title": "Smart Clip & Recorte CapCut",
    "features.card3_desc": "Ajusta los tiempos de inicio y fin con un deslizador visual interactivo. Extrae solo el fragmento de video o audio que necesitas (15s, 30s, 60s o personalizado).",
    "features.card4_title": "Másters de Audio (MP3 320k & WAV)",
    "features.card4_desc": "Extrae pistas sonoras independientes en la máxima fidelidad disponible: MP3 a 320 kbps o formato WAV sin compresión para producción de audio.",
    "features.card5_title": "Subtítulos & +1000 Plataformas Soportadas",
    "features.card5_desc": "Exporta subtítulos nativos y auto-generados en formatos .SRT, .VTT o .TXT. Compatible con YouTube, TikTok, Instagram, Twitter/X, Vimeo, Twitch y cientos de plataformas globales.",

    // Steps
    "steps.badge": "Flujo de trabajo",
    "steps.title": "Tres pasos simples.",
    "steps.sub": "Procesamiento transparente sin instalaciones ni registros.",
    "steps.step1_tag": "Paso 01",
    "steps.step1_title": "Ingresa la fuente",
    "steps.step1_desc": "Pega la URL de tu video o playlist, o selecciona un archivo local directamente desde tu dispositivo.",
    "steps.step2_tag": "Paso 02",
    "steps.step2_title": "Configura el formato",
    "steps.step2_desc": "Selecciona la calidad (4K, 1080p, Audio HD), ajusta los tiempos de corte si deseas un clip y revisa el resumen lateral.",
    "steps.step3_tag": "Paso 03",
    "steps.step3_title": "Procesa y Descarga",
    "steps.step3_desc": "Velo procesa el archivo de manera asíncrona mediante FFmpeg en la nube y lo envía directamente a tu navegador.",

    // FAQ
    "faq.title": "Preguntas frecuentes",
    "faq.q1": "¿Qué plataformas soporta Velo?",
    "faq.a1": "Velo utiliza yt-dlp como motor principal de extracción, lo que le permite trabajar con más de 1000 sitios web incluyendo YouTube, Vimeo, Twitter/X, Instagram, TikTok, Facebook, Dailymotion, Twitch, SoundCloud y muchos más.",
    "faq.q2": "¿Cómo funcionan las descargas masivas o de playlists?",
    "faq.a2": "Al seleccionar la pestaña \"Lista / Playlist\", puedes ingresar múltiples URLs o el enlace de una lista completa. Velo procesa cada elemento en el servidor y te entrega un único archivo comprimido .ZIP listo para guardar.",
    "faq.q3": "¿Puedo recortar solo un fragmento de un video?",
    "faq.a3": "Sí. Activa la opción de recorte en las opciones avanzadas para usar el deslizador interactivo o los botones de atajo (15s, 30s, 60s). Velo cortará el video o audio de forma exacta sin descargar datos innecesarios.",
    "faq.q4": "¿Cómo descargo solo los subtítulos de un video?",
    "faq.a4": "En el panel de opciones avanzadas se detectan los subtítulos disponibles (manuales o auto-generados). Puedes seleccionar el idioma y exportar el archivo directamente en formato .SRT, .VTT o .TXT.",
    "faq.q5": "¿Velo almacena mis descargas o datos personales?",
    "faq.a5": "No. Los archivos se procesan de forma temporal en el servidor durante la transferencia y se eliminan de forma inmediata. No se recopilan datos personales, historial de uso ni cookies de rastreo.",
    "faq.q6": "¿Velo es gratuito?",
    "faq.a6": "Sí. Velo es 100% gratuito, libre de publicidad, sin suscripciones obligatorias ni limitaciones ocultas.",

    // Support
    "donate.title": "Apoya el proyecto Velo",
    "donate.desc": "Velo es 100% gratuito, libre de publicidad y sin suscripciones. Si te resulta útil y deseas contribuir a mantener los servidores activos, cualquier donación voluntaria es profundamente apreciada.",

    // CTA & Footer
    "cta.title": "Empieza a descargar sin fricción.",
    "cta.sub": "Sin anuncios. Sin cuentas. Sin limites de velocidad.",
    "cta.btn": "Usar Velo Ahora",
    "footer.tagline": "Plataforma multimedia directa, privada y de alta velocidad.",
    "footer.status": "Todos los sistemas operacionales"
  },
  en: {
    // Navbar
    "nav.features": "Features",
    "nav.process": "Workflow",
    "nav.faq": "FAQ",
    "nav.donate": "Donate",
    "nav.cta": "Use Velo",

    // Hero
    "hero.badge_tag": "Velo v2.0",
    "hero.badge_text": "New SaaS Architecture: Bulk .ZIP Downloads, CapCut Trimming & HD Audio",
    "hero.title_1": "Download & process media",
    "hero.title_2": "in original quality.",
    "hero.subtitle": "A high-performance complete multimedia suite. Inspect 4K resolutions, trim clips in real time, extract high-fidelity audio, and download full playlists into .ZIP archives.",
    "hero.btn_app": "Open Velo App",
    "hero.btn_features": "Explore v2.0 Features",
    "hero.platforms": "Native support for YouTube, TikTok, Instagram, Twitter/X, Vimeo, Twitch, and 1000+ sites",

    // App Section
    "app.title": "Velo App — Downloader & Processor",
    "app.mode_single": "Single URL",
    "app.mode_batch": "Playlist / Batch (.ZIP)",
    "app.mode_local": "Local File",
    "app.url_placeholder": "Paste video, audio, or playlist URL here...",
    "app.paste": "Paste",
    "app.inspect": "Inspect",
    "app.batch_placeholder": "Paste multiple URLs (one per line)...",
    "app.batch_btn": "Process Batch (.ZIP)",
    "app.local_drop": "Drag & drop a video/audio file here or click to browse",
    "app.detected_badge": "Media Detected",

    // Download Types
    "app.type_title": "2. Choose export target",
    "app.type_combo_title": "Video + audio",
    "app.type_combo_desc": "Full media content in HD / 4K quality",
    "app.type_audio_title": "Audio only",
    "app.type_audio_desc": "Extract music or podcast tracks (MP3/WAV)",
    "app.type_video_title": "Video only",
    "app.type_video_desc": "Muted video stream without audio track",
    "app.webm_compatibility": "WebM Compatibility",

    // Resolutions & Formats
    "app.formats_title": "3. Available quality",
    "app.empty_formats": "No downloadable formats found for this category.",

    // Advanced Options
    "app.toggle_advanced": "Show advanced options",
    "app.toggle_advanced_hide": "Hide advanced options",
    "app.subtitles_label": "Extract Subtitles",
    "app.subtitles_lang": "Subtitle language:",
    "app.trim_label": "Trim Clip (CapCut Style)",
    "app.gif_label": "Convert to Animated GIF",
    "app.gif_btn": "Export as GIF",

    // Summary Card
    "summary.title": "Export Summary",
    "summary.waiting_link": "Waiting for URL...",
    "summary.inspect_prompt": "Inspect a URL",
    "summary.type": "Download type:",
    "summary.quality": "Selected quality:",
    "summary.format": "Final format:",
    "summary.size": "Estimated size:",
    "summary.tools": "Active tools:",
    "summary.checklist_title": "Pre-flight Validation Checklist",
    "summary.check_url": "Verified URL",
    "summary.check_quality": "Quality Selected",
    "summary.check_config": "Configuration Complete",
    "summary.btn_download": "Start Download",
    "summary.microcopy": "You can verify the filename and save location before storing.",
    "summary.pending": "Pending selection",
    "summary.none": "None",

    // Bento Grid Features
    "features.badge": "v2.0 Capabilities",
    "features.main_title": "Built for extreme speed.<br>No middleman.",
    "features.main_sub": "High-performance asynchronous architecture optimized for the modern web.",
    "features.card1_title": "2-Column SaaS Layout with Sticky Summary",
    "features.card1_desc": "Optimized dual-column workspace: control panel on the left and floating sticky summary card on the right with automated pre-flight validation.",
    "features.card2_title": "Bulk Batch Downloads (.ZIP)",
    "features.card2_desc": "Download full playlists and multi-link batches in parallel, automatically packaged into a single compressed .ZIP archive.",
    "features.card3_title": "Smart Clip & CapCut Trimming",
    "features.card3_desc": "Adjust start and end times with an interactive visual range slider. Extract only the exact video/audio clip you need (15s, 30s, 60s, or custom).",
    "features.card4_title": "Master Audio Streams (MP3 320k & WAV)",
    "features.card4_desc": "Extract standalone audio tracks in peak fidelity: 320kbps MP3 or uncompressed WAV format for audio post-production.",
    "features.card5_title": "Subtitles & 1000+ Platforms Supported",
    "features.card5_desc": "Export native and auto-generated transcripts in .SRT, .VTT, or .TXT formats. Compatible with YouTube, TikTok, Instagram, Twitter/X, Vimeo, Twitch, and global platforms.",

    // Steps
    "steps.badge": "Workflow",
    "steps.title": "Three simple steps.",
    "steps.sub": "Transparent processing without software installs or signups.",
    "steps.step1_tag": "Step 01",
    "steps.step1_title": "Input the Source",
    "steps.step1_desc": "Paste your video/playlist URL, or drop a local media file directly from your computer.",
    "steps.step2_tag": "Step 02",
    "steps.step2_title": "Configure Format",
    "steps.step2_desc": "Select media quality (4K, 1080p, HD Audio), adjust clip timestamps if needed, and review the summary panel.",
    "steps.step3_tag": "Step 03",
    "steps.step3_title": "Process & Download",
    "steps.step3_desc": "Velo processes the media stream asynchronously via FFmpeg in the cloud and delivers it to your browser.",

    // FAQ
    "faq.title": "Frequently Asked Questions",
    "faq.q1": "What platforms does Velo support?",
    "faq.a1": "Velo uses yt-dlp as its primary extraction engine, enabling compatibility with 1000+ websites including YouTube, Vimeo, Twitter/X, Instagram, TikTok, Facebook, Dailymotion, Twitch, SoundCloud, and more.",
    "faq.q2": "How do bulk playlist downloads work?",
    "faq.a2": "When selecting the \"Playlist / Batch\" tab, you can enter multiple URLs or a full playlist link. Velo processes each item on the server and delivers a single compressed .ZIP file ready to save.",
    "faq.q3": "Can I trim just a section of a video?",
    "faq.a3": "Yes. Enable clip trimming in advanced options to use the visual slider or shortcut buttons (15s, 30s, 60s). Velo cuts the exact video or audio clip without downloading unnecessary data.",
    "faq.q4": "How do I download only subtitles?",
    "faq.a4": "Available transcripts (official or auto-generated) are detected in advanced options. You can choose the target language and export the subtitle file in .SRT, .VTT, or .TXT format.",
    "faq.q5": "Does Velo store my downloads or personal data?",
    "faq.a5": "No. Files are processed temporarily on the server during transfer and deleted immediately after. No personal data, usage history, or tracking cookies are collected.",
    "faq.q6": "Is Velo free to use?",
    "faq.a6": "Yes. Velo is 100% free, ad-free, with no required subscriptions or hidden limits.",

    // Support
    "donate.title": "Support the Velo Project",
    "donate.desc": "Velo is 100% free, ad-free, and subscription-free. If you find it useful and want to help keep the servers running, voluntary donations are deeply appreciated.",

    // CTA & Footer
    "cta.title": "Start downloading friction-free.",
    "cta.sub": "No ads. No accounts. No speed limits.",
    "cta.btn": "Use Velo Now",
    "footer.tagline": "Direct, private, high-speed multimedia platform.",
    "footer.status": "All systems operational"
  }
};
