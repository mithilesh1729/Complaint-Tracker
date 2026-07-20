# We use multi-stage build to first build the frontend, then serve it with Nginx
FROM node:20-alpine AS build-stage

WORKDIR /app

# We need to build the frontend
# Since we are building from the root directory context, 
# we need to copy the frontend files
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# Nginx stage
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/

# Copy built frontend files
COPY --from=build-stage /app/dist /usr/share/nginx/html

# We also need to copy Django static files from the backend image
# But Docker Compose build context doesn't easily allow cross-image copying in standard ways without complex setups
# So we'll build the static files in the backend and use a shared volume, OR copy them here
# Actually, the simplest way is to let Nginx serve the frontend and let Django serve its own static files via WhiteNoise
# Wait, WhiteNoise is not installed.
# We will copy Django static files from the backend container at runtime using a volume? No, best to build them here too or use a multi-stage approach if possible.
# Wait! In docker-compose.prod.yml, we can just share a volume for static files or let nginx copy them.
# The standard approach is to use a volume for static files, but let's just use WhiteNoise in prod.py? 
# No, let's stick to the plan: run collectstatic in backend, and share a volume for static files.
# Wait, I didn't add a static volume in docker-compose.prod.yml. I should add it!
