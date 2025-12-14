const CACHE_NAME = 'rubix-v2';
const urlsToCache = [
    '/',
    '/index.html',
    '/manifest.json',
    '/favicon.png', // Fallback
    '/icons/icon-192x192.png',
    '/icons/icon-512x512.png',
    '/index.css'
];

self.addEventListener('install', (event) => {
    // Force new SW to take control immediately
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

self.addEventListener('activate', (event) => {
    // Clear old caches
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Stale-while-revalidate strategy
    event.respondWith(
        caches.match(event.request)
            .then((cachedResponse) => {
                const fetchPromise = fetch(event.request).then((networkResponse) => {
                    // Update cache with new response
                    // EXCLUDE ADS & TRACKERS from Cache
                    const url = event.request.url;
                    const isAd = url.includes('adsterra') || url.includes('google') || url.includes('doubleclick') || url.includes('analytics');

                    if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic' && !isAd) {
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                    }
                    return networkResponse;
                });
                // Return cached response immediately if available, else wait for network
                return cachedResponse || fetchPromise;
            })
    );
});
