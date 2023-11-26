module.exports = {
  apps: [
    {
      name: "alphastocks_frontend",
      script: "npm",
      args: "start",
      env: {
        NODE_ENV: "production",
        PORT: 3003,
      },
    },
  ],
};
