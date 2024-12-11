FROM node:20 AS node-builder

WORKDIR /app
COPY . .
RUN npm install -g pnpm && \
    pnpm install && \
    pnpm build

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
COPY app ./app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Node.js build artifacts and dependencies
COPY --from=node-builder /app/dist ./dist
COPY --from=node-builder /app/node_modules ./node_modules
COPY --from=node-builder /app/package.json ./

# Copy environment variables
COPY .env ./

ENV PORT=8080
EXPOSE 8080

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
