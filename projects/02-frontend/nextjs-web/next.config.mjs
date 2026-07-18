/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // The dashboard proxies API calls through Next.js route handlers to avoid CORS.
  env: {
    API_URL: process.env.API_URL ?? "http://localhost:8080",
  },
};

export default nextConfig;
