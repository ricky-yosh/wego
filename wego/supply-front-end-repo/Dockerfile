# syntax=docker/dockerfile:1

ARG NODE_VERSION=20.11.1

FROM node:${NODE_VERSION}-alpine

# Use production node environment by default.
ENV NODE_ENV local
WORKDIR /usr/src/app

# Copy package.json and package-lock.json into the image.
COPY package*.json ./

# # Clear npm cache
# RUN npm cache clean --force

# # Install dependencies using npm ci.
#TODO RUN npm ci --omit=dev
RUN npm install

# Copy the rest of your app's source code
COPY . .

# Expose the port that the application listens on.
EXPOSE 3000

#TODO Run the application as a non-root user.
# USER node

# Run the application.
CMD npm run dev