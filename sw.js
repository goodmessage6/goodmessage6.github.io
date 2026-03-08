const CACHE_NAME = 'combat-chicken-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/skies/sky1.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/skies/starfield.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/tilemaps/tiles/kenny_platformer.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/tilemaps/tiles/kenny.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/chick.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/tomato.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/onion.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/eggplant.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/carrot.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/wasp.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/coin.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/sprites/firstaid.png',
  'https://cdn.jsdelivr.net/gh/samme/phaser-examples-assets@1.0.0/bullets/bullet12.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Opened cache');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
