# ---------- Build Stage ----------
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build


# ---------- Runtime Stage ----------
FROM node:18-alpine

WORKDIR /app

# Install lightweight static server
RUN npm install -g serve

# Create non-root user (SECURITY REQUIREMENT)
RUN addgroup -S app && adduser -S app -G app

# Copy build output only (clean + optimized)
COPY --from=builder /app/build ./build

USER app

EXPOSE 3000

# Production serving
CMD ["serve", "-s", "build", "-l", "3000"] 