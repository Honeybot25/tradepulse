/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.tradepulse.app/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
