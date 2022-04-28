/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: "/api/:path*",
        destination: "https://shopbackend.honeycombpizza.link/api/:path*",
        permanent: false,
      },
    ];
  },
  async rewrites() {
    return [
      {
        source: "/cliserver/:path*",
        destination: "https://blog.honeycombpizza.link/cliserver/:path*",
      },
    ];
  },
};
