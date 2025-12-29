const CACHE_NAME = 'escolar-v5'; // Subimos a v5
const assets = [
  '/',
  '/static/manifest.json',
  '/static/logo.jpeg' // CAMBIO: Debe ser igual al del manifest.json
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      // Intentamos cachear los archivos, si falla uno, no se instala
      return cache.addAll(assets);
    })
  );
  self.skipWaiting(); 
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;

  e.respondWith(
    caches.match(e.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(e.request).catch(() => {
        // Si no hay red y es una navegación, forzamos el inicio
        if (e.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});