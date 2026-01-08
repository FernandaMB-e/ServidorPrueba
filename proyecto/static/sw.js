const CACHE_NAME = 'escolar-v10'; // Subimos a v9 para forzar la actualización
const assets = [
  '/',
  '/static/manifest.json',
  '/static/logo.jpeg' 
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(assets).catch(err => console.log("Error en cacheo inicial:", err));
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
  // Solo manejamos peticiones GET
  if (e.request.method !== 'GET') return;

  // ESTRATEGIA: Cache First (Priorizar Caché)
  // Esto hace que la carga sea instantánea aunque el servidor esté apagado
  e.respondWith(
    caches.match(e.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse; // Si está en caché, lo devuelve de inmediato
      }

      // Si no está en caché, intenta buscarlo en la red
      return fetch(e.request).then(networkResponse => {
        // Opcional: podrías guardar nuevas peticiones en caché aquí
        return networkResponse;
      }).catch(() => {
        // Si falla la red y es una navegación, mostramos la raíz
        if (e.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});