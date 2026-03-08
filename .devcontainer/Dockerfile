FROM mcr.microsoft.com/devcontainers/javascript-node:1-20-bookworm

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    default-mysql-client \
  && rm -rf /var/lib/apt/lists/*