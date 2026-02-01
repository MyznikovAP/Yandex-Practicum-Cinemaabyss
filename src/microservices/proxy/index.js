const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Health endpoint
app.get('/health', (req, res) => {
  res.json({ status: true, hello: 'qq' });
});

// Environment variables for downstream services
const MONOLITH_URL = process.env.MONOLITH_URL || 'http://localhost:8080';
const MOVIES_SERVICE_URL = process.env.MOVIES_SERVICE_URL || 'http://localhost:8081';
const EVENTS_SERVICE_URL = process.env.EVENTS_SERVICE_URL || 'http://localhost:8082';
// Feature flags for gradual migration
const GRADUAL_MIGRATION = process.env.GRADUAL_MIGRATION === "true";
const MOVIES_MIGRATION_PERCENT = parseInt(process.env.MOVIES_MIGRATION_PERCENT || "0", 10);

// Helper to create proxy based on path prefix
function proxyPath(pathPrefix, target) {
  app.use(pathPrefix, createProxyMiddleware({
    target,
    changeOrigin: true,

    onProxyReq: (proxyReq, req, res) => {
      proxyReq.setHeader('host', new URL(target).host);
    },
  }));
}

function proxyGradualPath(pathPrefix, target, proxyTarget) {
  app.use(pathPrefix, createProxyMiddleware({
    router: (req) => {
      if (GRADUAL_MIGRATION) {
        const migrationChoice = Math.random() * 100;
        // Инвертированная логика: если условие выполняется, идем на proxyTarget
        return migrationChoice < MOVIES_MIGRATION_PERCENT 
          ? proxyTarget  // Новый сервер
          : target;      // Старый сервер
      }
      // По умолчанию всегда на proxyTarget (новый сервер)
      return proxyTarget;
    },
    changeOrigin: true,
  }));
}

// Proxy routes
proxyPath('/api/users', MONOLITH_URL);
proxyPath('/api/payments', MONOLITH_URL);
proxyPath('/api/subscriptions', MONOLITH_URL);
// Conditional proxy for movies with gradual migration support
proxyGradualPath('/api/movies', MONOLITH_URL, MOVIES_SERVICE_URL);
proxyPath('/api/events', EVENTS_SERVICE_URL);

// Start server
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
  console.log(`Proxy service listening on port ${PORT}`);
});
