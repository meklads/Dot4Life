FROM node:18-alpine
WORKDIR /app
COPY capsule-engine/package*.json ./
RUN npm install --production
COPY capsule-engine/ .
EXPOSE 3030
CMD ["node", "server.js"]
