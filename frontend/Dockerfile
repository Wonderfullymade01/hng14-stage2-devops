# Stage 1
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Stage 2
FROM node:18-alpine
WORKDIR /app
RUN adduser -D appuser
USER appuser

COPY --from=builder /app /app

EXPOSE 3000

CMD ["npm", "start"]