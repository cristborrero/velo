// Velo PWA Service Worker v3.0.1
const CACHE_NAME = 'velo-v3.0.1';
const ASSETS = [
  '/',
  '/static/style.css',
  '/static/app.js',
  '/static/logo.svg',
  '/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const requestPath = new URL(event.request.url).pathname;

  // Always prefer a fresh app shell so clients receive polling fixes promptly.
  if (requestPath === '/static/app.js') {
    event.respondWith(
      fetch(event.request).then((response) => {
        if (!response.ok) return response;
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, response.clone());
          return response;
        });
      }).catch(() => caches.match(event.request))
    );
    return;
  }
  
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return (
        cached ||
        fetch(event.request).then((response) => {
          return caches.open(CACHE_NAME).then((cache) => {
            if (event.request.url.startsWith('http')) {
              cache.put(event.request, response.clone());
            }
            return response;
          });
        })
      );
    }).catch(() => caches.match('/'))
  );
});
