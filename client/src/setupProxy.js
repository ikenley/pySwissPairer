const { createProxyMiddleware } = require("http-proxy-middleware");

// Proxy server can point to either localhost for debugging or the dev endpoint
// This could be ENV var based eventually, but it's easy + safe to store in git
const debugApi = false;
const isProd = false;

const devHost = "https://predictions.ikenley.com";
const prodHost = "https://predictions.ikenley.com";
const remoteHost = isProd ? prodHost : devHost;

const apiTarget = debugApi ? "http://localhost:5000" : remoteHost;

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: apiTarget,
      changeOrigin: true,
    })
  );
};
