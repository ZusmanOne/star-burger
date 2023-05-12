FROM node:16.0-alpine
WORKDIR /usr/src/app
COPY *.json ./
RUN npm install
COPY . /usr/src/app
RUN npm ci --include=dev instead
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
