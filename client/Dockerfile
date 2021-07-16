# Multi-stage
# 1) Node image for building frontend assets
# 2) nginx stage to serve frontend assets
# https://typeofnan.dev/how-to-serve-a-react-app-with-nginx-in-docker/

# Name the node stage "builder"
FROM node:15 AS builder
# Set IMAGE_TAG ENV var
ARG IMAGE_TAG
ENV REACT_APP_IMAGE_TAG=$IMAGE_TAG
# Set working directory
WORKDIR /app
# Copy all files from current directory to working dir in image
COPY . .
# install node modules and build assets
RUN npm install && npm run build

# nginx state for serving content
FROM nginx:alpine
# Copy nginx conf
ARG BRANCH_NAME
COPY nginx/${BRANCH_NAME}/nginx.conf /etc/nginx/nginx.conf
# Set working directory to nginx asset directory
WORKDIR /usr/share/nginx/html
# Remove default nginx static assets
RUN rm -rf ./*
# Copy static assets from builder stage
COPY --from=builder /app/build .
# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]