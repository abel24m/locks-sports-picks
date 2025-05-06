import type { NextConfig } from "next";

const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/:path*',
        destination : process.env.REACT_APP_API_URL,
      },
    ]
  },
};


export default nextConfig;
