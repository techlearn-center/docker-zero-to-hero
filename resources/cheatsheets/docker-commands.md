# Docker Commands Cheat Sheet

Quick reference for the most commonly used Docker commands.

---

## Images

```bash
# Build an image from a Dockerfile
docker build -t <name>:<tag> .

# Build with a specific Dockerfile
docker build -f Dockerfile.prod -t <name>:<tag> .

# List local images
docker images

# Remove an image
docker rmi <image>

# Remove all unused images
docker image prune

# Tag an image
docker tag <source> <target>:<tag>

# Push to a registry
docker push <name>:<tag>

# Pull from a registry
docker pull <name>:<tag>

# Inspect image details
docker inspect <image>

# View image history (layers)
docker history <image>
```

---

## Containers

```bash
# Run a container
docker run <image>

# Run in background (detached)
docker run -d <image>

# Run with port mapping
docker run -p <host>:<container> <image>

# Run with a name
docker run --name <name> <image>

# Run with environment variables
docker run -e KEY=value <image>

# Run interactively
docker run -it <image> sh

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a container
docker stop <container>

# Start a stopped container
docker start <container>

# Restart a container
docker restart <container>

# Remove a container
docker rm <container>

# Force remove a running container
docker rm -f <container>

# Remove all stopped containers
docker container prune

# View container logs
docker logs <container>

# Follow logs in real-time
docker logs -f <container>

# Execute a command inside a running container
docker exec -it <container> sh

# Copy files between host and container
docker cp <container>:/path /host/path
docker cp /host/path <container>:/path

# View container resource usage
docker stats

# Inspect container details
docker inspect <container>
```

---

## Volumes

```bash
# Create a named volume
docker volume create <name>

# List volumes
docker volume ls

# Inspect a volume
docker volume inspect <name>

# Remove a volume
docker volume rm <name>

# Remove all unused volumes
docker volume prune

# Run with a named volume
docker run -v <volume>:/path <image>

# Run with a bind mount
docker run -v /host/path:/container/path <image>
```

---

## Networks

```bash
# Create a network
docker network create <name>

# List networks
docker network ls

# Inspect a network
docker network inspect <name>

# Remove a network
docker network rm <name>

# Connect a container to a network
docker network connect <network> <container>

# Disconnect a container from a network
docker network disconnect <network> <container>

# Run a container on a specific network
docker run --network <network> <image>
```

---

## Docker Compose

```bash
# Start all services (background)
docker compose up -d

# Start and rebuild images
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View running services
docker compose ps

# View logs
docker compose logs

# Follow logs
docker compose logs -f

# View logs for one service
docker compose logs <service>

# Restart a service
docker compose restart <service>

# Execute command in a service
docker compose exec <service> sh

# Build images without starting
docker compose build

# Pull images defined in compose file
docker compose pull

# Scale a service
docker compose up -d --scale <service>=3
```

---

## System / Cleanup

```bash
# View Docker disk usage
docker system df

# Remove all unused data (images, containers, networks)
docker system prune

# Remove everything including unused images
docker system prune -a

# Remove everything including volumes (DATA LOSS!)
docker system prune -a --volumes

# Docker version
docker --version

# Docker system info
docker info
```

---

## Dockerfile Instructions Reference

| Instruction | Purpose | Example |
|------------|---------|---------|
| `FROM` | Base image | `FROM node:18-alpine` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files into image | `COPY package.json .` |
| `ADD` | Copy files (supports URLs, tar extraction) | `ADD app.tar.gz /app` |
| `RUN` | Execute command during build | `RUN npm install` |
| `CMD` | Default command when container starts | `CMD ["node", "app.js"]` |
| `ENTRYPOINT` | Main executable | `ENTRYPOINT ["node"]` |
| `EXPOSE` | Document exposed port | `EXPOSE 3000` |
| `ENV` | Set environment variable | `ENV NODE_ENV=production` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `VOLUME` | Create mount point | `VOLUME /data` |
| `USER` | Set the user | `USER appuser` |
| `HEALTHCHECK` | Container health check | `HEALTHCHECK CMD curl -f http://localhost/` |
| `LABEL` | Add metadata | `LABEL version="1.0"` |

---

## Common Patterns

### Development Container

```bash
docker run -dp 3000:3000 \
  -v "$(pwd):/app" \
  -v /app/node_modules \
  -w /app \
  node:18-alpine \
  sh -c "npm install && npx nodemon src/index.js"
```

### Multi-Container with Network

```bash
# Create network
docker network create mynet

# Start database
docker run -d --name db --network mynet \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8.0

# Start app
docker run -dp 3000:3000 --network mynet \
  -e DB_HOST=db \
  myapp
```

### Quick Debug / Explore

```bash
# Jump into a running container
docker exec -it <container> sh

# Run a throwaway container for debugging
docker run --rm -it alpine sh

# Check what's in an image
docker run --rm <image> ls -la /app
```

---

**[Back to Workshop Home](../../README.md)**
