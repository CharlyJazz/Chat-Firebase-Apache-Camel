# https://github.com/vercel/next.js/blob/canary/examples/with-docker/Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

# Rebuild the source code only when needed
FROM node:18-alpine AS builder

WORKDIR /app

COPY . .
COPY --from=deps /app/node_modules ./node_modules

RUN NEXT_PUBLIC_AUTH_MICROSERVICE=NEXT_PUBLIC_AUTH_MICROSERVICE NEXT_PUBLIC_CHAT_MICROSERVICE=NEXT_PUBLIC_CHAT_MICROSERVICE NEXT_PUBLIC_API_KEY=NEXT_PUBLIC_API_KEY NEXT_PUBLIC_AUTH_DOMAIN=NEXT_PUBLIC_AUTH_DOMAIN NEXT_PUBLIC_PROJECT_ID=NEXT_PUBLIC_PROJECT_ID NEXT_PUBLIC_STORAGE_BUCKET=NEXT_PUBLIC_STORAGE_BUCKET NEXT_PUBLIC_MESSAGING_SENDER_ID=NEXT_PUBLIC_MESSAGING_SENDER_ID NEXT_PUBLIC_APP_ID=NEXT_PUBLIC_APP_ID npm run build

# Production image, copy all the files and run next
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/entrypoint.sh ./entrypoint.sh

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
RUN chown -R nextjs:nodejs /app/.next

USER nextjs

EXPOSE 3000

RUN npx next telemetry disable

ENTRYPOINT ["/app/entrypoint.sh"]

CMD npm run start