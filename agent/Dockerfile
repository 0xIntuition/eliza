FROM node:20 AS node-builder

WORKDIR /app
# Copy package files for workspace
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/core/package.json ./packages/core/
COPY agent/package.json ./agent/

# Install dependencies
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

# Copy source files
COPY packages/core/src ./packages/core/src
COPY packages/core/tsconfig.json ./packages/core/
COPY packages/core/tsup.config.ts ./packages/core/
COPY agent/src ./agent/src
COPY agent/tsconfig.json ./agent/
COPY agent/tsup.config.ts ./agent/

# Build packages
RUN cd packages/core && pnpm run build && \
    cd ../../agent && pnpm run build

FROM python:3.12-slim

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm

WORKDIR /app

# Copy Python app and requirements
COPY agent/app ./app
COPY agent/requirements.txt .
COPY agent/pyproject.toml agent/poetry.lock ./

# Install Python dependencies using poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy Node.js build artifacts and dependencies
COPY --from=node-builder /app/agent/dist ./dist
COPY --from=node-builder /app/agent/node_modules ./node_modules
COPY --from=node-builder /app/agent/package.json ./

# Copy environment variables
COPY agent/.env ./

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
