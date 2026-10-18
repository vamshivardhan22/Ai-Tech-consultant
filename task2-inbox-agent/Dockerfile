FROM node:22-alpine
WORKDIR /app
COPY package*.json tsconfig.json ./
RUN npm install --no-audit --no-fund
COPY src ./src
RUN npm run build
RUN mkdir -p /data
ENV PORT=8002 INBOX_DATA_PATH=/data/feedback.json
EXPOSE 8002
CMD ["npm", "start"]
