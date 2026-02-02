# Docker Interview Preparation

A comprehensive guide covering Docker questions asked in DevOps, SRE, Backend, Cloud, and Platform Engineering interviews. Questions are organized by difficulty and topic.

---

## Beginner Level

### Fundamentals

<details>
<summary><strong>Q1: What is Docker and why is it used?</strong></summary>

Docker is a platform for building, shipping, and running applications in containers. Containers package an application with all its dependencies — libraries, runtime, system tools, and configuration — into a single portable unit.

**Why it's used:**
- Eliminates "works on my machine" problems
- Provides consistent environments across dev, staging, and production
- Enables microservices architecture
- Makes CI/CD pipelines reproducible
- Reduces infrastructure costs through efficient resource utilization

</details>

<details>
<summary><strong>Q2: What is the difference between a Docker image and a container?</strong></summary>

| Aspect | Image | Container |
|--------|-------|-----------|
| State | Read-only template | Running (or stopped) instance |
| Analogy | Class in OOP | Object/instance of the class |
| Storage | Layers on disk | Writable layer on top of image |
| Creation | Built from Dockerfile | Created from an image |
| Lifecycle | Persists until deleted | Ephemeral by default |

**Key point:** One image can create many containers. Each container has its own writable layer but shares the image's read-only layers.

</details>

<details>
<summary><strong>Q3: What is a Dockerfile? Walk me through a basic one.</strong></summary>

A Dockerfile is a text file containing instructions to build a Docker image. Each instruction creates a layer in the final image.

```dockerfile
FROM node:18-alpine    # Base image (starting point)
WORKDIR /app           # Set working directory
COPY package.json .    # Copy dependency manifest
RUN npm install        # Install dependencies (build-time)
COPY . .               # Copy application source
EXPOSE 3000            # Document which port the app uses
CMD ["node", "app.js"] # Default command at runtime
```

**Important distinctions:**
- `RUN` executes during build time (creates a layer)
- `CMD` defines the default command at runtime (doesn't create a layer)
- `EXPOSE` is documentation only — it doesn't actually publish the port

</details>

<details>
<summary><strong>Q4: What is the difference between CMD and ENTRYPOINT?</strong></summary>

| Aspect | CMD | ENTRYPOINT |
|--------|-----|------------|
| Purpose | Default command and/or arguments | Main executable |
| Override | Easily overridden by `docker run <args>` | Requires `--entrypoint` flag to override |
| Typical use | Providing defaults that can be changed | Defining the container's primary purpose |

**Example:**
```dockerfile
# With CMD (overridable):
CMD ["python", "app.py"]
# docker run myapp             → python app.py
# docker run myapp python test.py  → python test.py (CMD overridden)

# With ENTRYPOINT (fixed executable):
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run myapp             → python app.py
# docker run myapp test.py     → python test.py (only args change)
```

**Best practice:** Use `ENTRYPOINT` for the executable and `CMD` for default arguments.

</details>

<details>
<summary><strong>Q5: What is Docker Hub?</strong></summary>

Docker Hub is the default public registry for Docker images. It functions like GitHub but for container images.

**Key features:**
- Official images (curated by Docker: `node`, `python`, `mysql`, `nginx`)
- User/organization repositories
- Automated builds from GitHub/Bitbucket
- Vulnerability scanning
- Rate limiting on free tier (100 pulls/6hr for anonymous, 200 for authenticated)

**Alternatives:** GitHub Container Registry (ghcr.io), Amazon ECR, Google Artifact Registry, Azure Container Registry, Harbor (self-hosted).

</details>

<details>
<summary><strong>Q6: How do you run a Docker container?</strong></summary>

```bash
# Basic
docker run nginx

# Production-like
docker run -d \              # Detached (background)
  --name web \               # Container name
  -p 8080:80 \               # Port mapping (host:container)
  -v app-data:/data \        # Named volume
  -e ENV_VAR=value \         # Environment variable
  --restart unless-stopped \ # Restart policy
  nginx:1.25-alpine          # Image with specific tag
```

**Key flags explained:**
- `-d` — Detached mode (background)
- `-p host:container` — Port mapping
- `-v` — Volume mount
- `-e` — Environment variable
- `--name` — Assign a name
- `--rm` — Auto-remove when stopped
- `-it` — Interactive with terminal (for debugging)

</details>

---

### Images & Building

<details>
<summary><strong>Q7: What are Docker image layers? Why do they matter?</strong></summary>

Each instruction in a Dockerfile creates a read-only layer. Layers are stacked to form the final image.

**Why they matter:**
1. **Caching** — Unchanged layers are reused from cache, making builds faster
2. **Sharing** — Multiple images can share base layers, saving disk space
3. **Transfer** — Only changed layers need to be pushed/pulled

**Caching rule:** If a layer changes, all layers ABOVE it are rebuilt.

```
Layer 5: COPY . .          ← Changes every code edit → rebuilt
Layer 4: RUN npm install   ← Only if package.json changes
Layer 3: COPY package.json ← Only if package.json changes
Layer 2: WORKDIR /app      ← Almost never changes
Layer 1: FROM node:18      ← Almost never changes
```

**Best practice:** Order instructions from least-frequently to most-frequently changed.

</details>

<details>
<summary><strong>Q8: What is the difference between COPY and ADD?</strong></summary>

| Feature | COPY | ADD |
|---------|------|-----|
| Copy local files | Yes | Yes |
| Extract tar archives | No | Yes (auto-extracts) |
| Download from URLs | No | Yes |
| Best practice | Preferred for most cases | Only when you need tar extraction |

**Recommendation:** Always use `COPY` unless you specifically need `ADD`'s tar extraction or URL download features. `COPY` is more explicit and predictable.

</details>

<details>
<summary><strong>Q9: What is a .dockerignore file?</strong></summary>

`.dockerignore` tells Docker which files to exclude from the build context (the directory sent to the Docker daemon during `docker build`).

```
node_modules
.git
.env
*.md
.DS_Store
```

**Benefits:**
- **Faster builds** — Less data to transfer to the daemon
- **Smaller images** — Excluded files can't accidentally be copied
- **Security** — Prevents secrets (`.env`) from ending up in images

**Analogy:** Works exactly like `.gitignore` but for Docker builds.

</details>

---

## Intermediate Level

### Networking

<details>
<summary><strong>Q10: How do Docker containers communicate with each other?</strong></summary>

Containers on the same Docker network can communicate using **container names as hostnames** (Docker's built-in DNS resolution).

```bash
# Create a network
docker network create mynet

# Start containers on the same network
docker run -d --name db --network mynet mysql:8
docker run -d --name app --network mynet -e DB_HOST=db myapp
# "db" resolves to the MySQL container's IP
```

**Network types:**
| Type | Use Case |
|------|----------|
| `bridge` | Default; containers on same host communicate |
| `host` | Container uses host's network directly (no isolation) |
| `none` | No network access |
| `overlay` | Multi-host networking (Docker Swarm) |
| Custom bridge | Named network with DNS resolution |

**Key insight:** The default `bridge` network does NOT support DNS resolution. You must create a custom network for name-based communication.

</details>

<details>
<summary><strong>Q11: What is the difference between port exposing and port publishing?</strong></summary>

```dockerfile
EXPOSE 3000        # Documents the port (metadata only, does NOT open it)
```

```bash
docker run -p 3000:3000 myapp   # PUBLISHES the port (makes it accessible)
```

| Action | Effect |
|--------|--------|
| `EXPOSE` in Dockerfile | Documentation only; no network effect |
| `-p host:container` | Actually maps the port; makes it accessible from host |
| `-P` (capital P) | Publishes all EXPOSE'd ports to random host ports |

</details>

<details>
<summary><strong>Q12: Explain Docker networking between containers — how would you connect a web app to a database?</strong></summary>

**Approach 1: Docker Network (manual)**
```bash
docker network create app-net
docker run -d --name mysql --network app-net -e MYSQL_ROOT_PASSWORD=secret mysql:8
docker run -d --name web --network app-net -e DB_HOST=mysql -p 3000:3000 myapp
```

**Approach 2: Docker Compose (recommended)**
```yaml
services:
  web:
    build: .
    ports: ["3000:3000"]
    environment:
      DB_HOST: mysql
    depends_on: [mysql]
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
```

Compose automatically creates a network — services reference each other by name.

</details>

### Storage

<details>
<summary><strong>Q13: What are Docker volumes and why are they needed?</strong></summary>

Containers are **ephemeral** — their writable layer is deleted when the container is removed. Volumes provide **persistent storage** that survives container lifecycle.

**Three mount types:**

| Type | Command | Use Case |
|------|---------|----------|
| Named volume | `-v mydata:/data` | Database files, uploads, persistent data |
| Bind mount | `-v /host/path:/container/path` | Development (live code editing) |
| tmpfs | `--tmpfs /tmp` | Sensitive data, temp files (RAM only) |

**Named volumes are preferred for production** because:
- Managed by Docker (portable, platform-independent)
- Can be backed up with `docker volume` commands
- Work the same on Linux, macOS, and Windows

</details>

<details>
<summary><strong>Q14: What is the difference between a named volume and a bind mount?</strong></summary>

| Aspect | Named Volume | Bind Mount |
|--------|-------------|------------|
| Location | Docker-managed (`/var/lib/docker/volumes/`) | Any host directory you specify |
| Portability | Works on all platforms | Path depends on host OS |
| Management | `docker volume` commands | Manual (host filesystem) |
| Best for | Production data, databases | Development, config files |
| Syntax | `-v my-vol:/data` | `-v /home/user/data:/data` |
| Data initialized | Populated from container if empty | Overwrites container contents |

</details>

### Docker Compose

<details>
<summary><strong>Q15: What is Docker Compose and when would you use it?</strong></summary>

Docker Compose is a tool for defining and running multi-container applications using a YAML file (`docker-compose.yml`).

**When to use it:**
- Multi-container applications (web + db + cache)
- Development environments
- Testing environments
- CI/CD pipelines
- Any setup requiring multiple `docker run` commands

**Key benefit:** Replace 10+ `docker run` commands with a single `docker compose up -d`.

```yaml
services:
  web:
    build: .
    ports: ["3000:3000"]
    depends_on: [db, redis]
  db:
    image: postgres:15
    volumes: [pgdata:/var/lib/postgresql/data]
  redis:
    image: redis:7-alpine
volumes:
  pgdata:
```

</details>

<details>
<summary><strong>Q16: What does depends_on do? Does it wait for the service to be ready?</strong></summary>

`depends_on` controls **startup order** — it ensures one service starts before another.

**Important caveat:** It only waits for the container to **start**, NOT for the service to be **ready**. MySQL might take 10-30 seconds to initialize after the container starts.

**Solution for readiness:**
```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy  # Wait for health check
  db:
    image: mysql:8
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 30s
```

</details>

---

## Advanced Level

### Security

<details>
<summary><strong>Q17: What are Docker security best practices?</strong></summary>

1. **Use specific image tags** — `node:18-alpine` not `node:latest`
2. **Run as non-root user** — `USER appuser` in Dockerfile
3. **Use multi-stage builds** — No build tools in production image
4. **Scan images for vulnerabilities** — Trivy, Snyk, Docker Scout
5. **Use `.dockerignore`** — Prevent secrets from entering images
6. **Don't store secrets in images** — Use runtime env vars or Docker secrets
7. **Use read-only filesystems** — `docker run --read-only`
8. **Limit resources** — CPU and memory limits
9. **Keep base images updated** — Patch known vulnerabilities
10. **Use minimal base images** — Alpine or distroless

</details>

<details>
<summary><strong>Q18: How do you handle secrets in Docker?</strong></summary>

**Bad practices:**
```dockerfile
# NEVER do this:
ENV DB_PASSWORD=mysecret           # Visible in image history
COPY .env /app/.env                # Baked into the image
RUN echo "password=secret" > config # In a layer forever
```

**Good practices:**
```bash
# Runtime environment variables
docker run -e DB_PASSWORD=secret myapp

# Docker secrets (Swarm mode)
echo "secret" | docker secret create db_pass -

# .env file (not committed to git)
docker run --env-file .env myapp

# External secret managers
# (HashiCorp Vault, AWS Secrets Manager, etc.)
```

**Key principle:** Secrets should be injected at runtime, never baked into images.

</details>

<details>
<summary><strong>Q19: What is a multi-stage build and why use it?</strong></summary>

Multi-stage builds use multiple `FROM` statements. Each stage can use a different base image. Only the final stage becomes the production image.

```dockerfile
# Stage 1: Build (includes compilers, dev tools)
FROM node:18 AS build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build     # Compile TypeScript, bundle, etc.

# Stage 2: Production (minimal, no build tools)
FROM node:18-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Benefits:**
- Smaller images (no compilers, dev tools)
- Reduced attack surface
- Faster pulls and deployments
- Clean separation of build and runtime

**Size comparison:**
- Single-stage: ~900MB
- Multi-stage: ~120MB

</details>

### Architecture & Operations

<details>
<summary><strong>Q20: How would you debug a container that keeps crashing?</strong></summary>

**Step-by-step approach:**

```bash
# 1. Check logs
docker logs <container>
docker logs --tail 50 <container>

# 2. Check exit code
docker inspect <container> --format='{{.State.ExitCode}}'
# Exit 0 = normal, 1 = app error, 137 = OOM killed, 139 = segfault

# 3. Check resource usage
docker stats <container>

# 4. Override CMD to get a shell
docker run -it --entrypoint sh <image>

# 5. Inspect container details
docker inspect <container>

# 6. Check if it's an OOM issue
docker inspect <container> --format='{{.State.OOMKilled}}'

# 7. Run with verbose logging
docker run -e LOG_LEVEL=debug <image>
```

</details>

<details>
<summary><strong>Q21: Explain the difference between Docker and Kubernetes.</strong></summary>

| Aspect | Docker | Kubernetes |
|--------|--------|------------|
| What it is | Container runtime + tools | Container orchestration platform |
| Scale | Single host | Cluster of hosts |
| Scheduling | Manual (`docker run`) | Automatic (scheduler) |
| Self-healing | No (container dies = stays dead) | Yes (restarts failed pods) |
| Load balancing | Manual or Compose | Built-in (Services) |
| Scaling | Manual | Automatic (HPA) |
| Rolling updates | Manual | Built-in |
| When to use | Development, single-host apps | Production, multi-host, microservices |

**Analogy:** Docker is like running a single ship. Kubernetes is like managing a fleet.

</details>

<details>
<summary><strong>Q22: How would you optimize a Docker image that's 2GB?</strong></summary>

**Investigation:**
```bash
docker history myimage  # See which layers are largest
docker system df        # Overall disk usage
```

**Optimization checklist:**

| Technique | Potential Savings |
|-----------|-----------------|
| Switch to Alpine base | 800MB → 50MB |
| Multi-stage build | Remove build tools (~500MB) |
| `.dockerignore` (exclude node_modules, .git) | 100-500MB |
| `--production` flag | Remove dev dependencies (~100MB) |
| Combine RUN commands | Reduce layer count |
| Clean caches in same RUN | Remove package manager caches |
| Use `--no-cache` for pip | Remove pip cache |

**Example combined RUN:**
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

</details>

<details>
<summary><strong>Q23: What happens when you run `docker run hello-world`? Walk through the entire process.</strong></summary>

1. Docker CLI sends the `run` command to the Docker daemon via REST API
2. Daemon checks if `hello-world:latest` image exists locally
3. If not found → pulls from Docker Hub (registry)
   - Resolves the tag to a specific digest
   - Downloads each layer (if not already cached)
4. Creates a container from the image
   - Allocates a writable layer on top of image layers
   - Sets up networking (bridge network by default)
   - Assigns an IP address
5. Runs the CMD defined in the image
   - The hello-world binary prints its message to stdout
6. Process exits → container moves to "stopped" state
7. Container remains in stopped state until removed with `docker rm`

</details>

<details>
<summary><strong>Q24: How do you implement health checks in Docker?</strong></summary>

**In Dockerfile:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 --start-period=10s \
  CMD curl -f http://localhost:3000/healthz || exit 1
```

**In docker-compose.yml:**
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/healthz"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```

**Health states:**
- `starting` — Within start_period, not yet checked
- `healthy` — Last N checks passed
- `unhealthy` — Last N checks failed

**Why it matters:** Health checks enable `depends_on: condition: service_healthy`, restart policies, and load balancer integration.

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>Q25: Your Docker build takes 10 minutes. How would you speed it up?</strong></summary>

1. **Fix layer ordering** — Put least-changing instructions first
2. **Use `.dockerignore`** — Reduce build context size
3. **Separate dependency install from code copy:**
   ```dockerfile
   COPY package.json .
   RUN npm install
   COPY . .     # Only this layer rebuilds on code changes
   ```
4. **Use BuildKit** — `DOCKER_BUILDKIT=1 docker build .`
5. **Use a faster base image** — Alpine instead of Ubuntu
6. **Cache mount for package managers:**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.npm npm install
   ```
7. **Multi-stage build** — Smaller final image = faster push

</details>

<details>
<summary><strong>Q26: A container is consuming too much memory and gets OOM-killed. How do you handle this?</strong></summary>

1. **Diagnose:**
   ```bash
   docker inspect <id> --format='{{.State.OOMKilled}}'  # Confirm OOM
   docker stats  # See real-time resource usage
   ```

2. **Set memory limits:**
   ```bash
   docker run -m 512m --memory-swap 1g myapp
   ```

3. **In Compose:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 512M
   ```

4. **Fix the root cause:**
   - Profile the application for memory leaks
   - Optimize data processing (streaming vs loading all into memory)
   - Check for known issues in the runtime (e.g., Node.js `--max-old-space-size`)

</details>

<details>
<summary><strong>Q27: You need to deploy a web app, database, and cache. Design the Docker architecture.</strong></summary>

```yaml
services:
  web:
    build: .
    ports: ["443:3000"]
    environment:
      DB_HOST: postgres
      REDIS_HOST: redis
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M

  postgres:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
    restart: unless-stopped

volumes:
  pgdata:
  redis-data:
```

**Key design decisions:**
- Named volumes for data persistence
- Health checks for startup ordering
- Memory limits to prevent resource exhaustion
- `restart: unless-stopped` for auto-recovery
- Secrets management (not hardcoded passwords)

</details>

<details>
<summary><strong>Q28: How would you set up a CI/CD pipeline that builds and deploys Docker images?</strong></summary>

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run tests
        run: docker run --rm myapp:${{ github.sha }} npm test

      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}

      - name: Login to registry
        run: echo "${{ secrets.REGISTRY_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

      - name: Push image
        run: |
          docker tag myapp:${{ github.sha }} ghcr.io/myorg/myapp:${{ github.sha }}
          docker tag myapp:${{ github.sha }} ghcr.io/myorg/myapp:latest
          docker push ghcr.io/myorg/myapp:${{ github.sha }}
          docker push ghcr.io/myorg/myapp:latest

      - name: Deploy
        run: |
          # Update Kubernetes deployment, ECS task, etc.
          kubectl set image deployment/myapp myapp=ghcr.io/myorg/myapp:${{ github.sha }}
```

</details>

---

## Quick-Fire Round

These are typically asked rapid-fire in interviews:

| Question | Answer |
|----------|--------|
| How do you stop all running containers? | `docker stop $(docker ps -q)` |
| How do you remove all stopped containers? | `docker container prune` |
| How do you remove all unused images? | `docker image prune -a` |
| How do you view logs of a running container? | `docker logs -f <container>` |
| How do you get a shell inside a running container? | `docker exec -it <container> sh` |
| What's the default network driver? | `bridge` |
| What does `-d` flag do? | Runs container in detached (background) mode |
| Difference between `docker stop` and `docker kill`? | `stop` sends SIGTERM (graceful), `kill` sends SIGKILL (immediate) |
| What is a dangling image? | An image with no tag (`<none>:<none>`), typically from rebuilds |
| How do you check image layers? | `docker history <image>` |

---

**[Back to Workshop Home](../README.md)**
