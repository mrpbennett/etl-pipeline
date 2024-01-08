# Use a Node.js image to build the app
FROM node:latest as build

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

EXPOSE 5173 

CMD ["npm", "run", "dev"] 