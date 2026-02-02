# Docker Compose Cheat Sheet

Quick reference for Docker Compose syntax and commands.

---

## CLI Commands

```bash
# Start services
docker compose up              # Foreground (see logs)
docker compose up -d           # Background (detached)
docker compose up -d --build   # Rebuild images first

# Stop services
docker compose down            # Stop and remove containers + network
docker compose down -v         # Also remove volumes (DATA LOSS!)
docker compose stop            # Stop without removing

# Status
docker compose ps              # List running services
docker compose top             # Show running processes

# Logs
docker compose logs            # All service logs
docker compose logs -f         # Follow logs (real-time)
docker compose logs web        # Specific service logs
docker compose logs --tail=50  # Last 50 lines

# Execute
docker compose exec web sh     # Shell into running container
docker compose run web npm test # Run one-off command

# Build
docker compose build           # Build all images
docker compose build web       # Build specific service
docker compose pull            # Pull latest images

# Cleanup
docker compose rm              # Remove stopped containers
docker compose down --rmi all  # Remove images too
```

---

## docker-compose.yml Structure

```yaml
# Minimal example
services:
  web:
    build: ./app
    ports:
      - "3000:3000"

  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

---

## Service Configuration

### Build from Dockerfile

```yaml
services:
  web:
    # Simple: build context only
    build: ./app

    # Detailed: specify Dockerfile
    build:
      context: ./app
      dockerfile: Dockerfile.prod
      args:
        NODE_ENV: production
```

### Use Pre-Built Image

```yaml
services:
  db:
    image: mysql:8.0
    # or
    image: ghcr.io/myorg/myapp:1.0
```

### Ports

```yaml
services:
  web:
    ports:
      - "3000:3000"          # host:container
      - "8080:80"            # different port mapping
      - "127.0.0.1:3000:3000" # bind to localhost only
```

### Environment Variables

```yaml
services:
  web:
    # Inline
    environment:
      NODE_ENV: production
      DB_HOST: db
      DB_PORT: 5432

    # From file
    env_file:
      - .env
      - .env.local
```

### Volumes

```yaml
services:
  web:
    volumes:
      # Named volume
      - app-data:/app/data

      # Bind mount (development)
      - ./src:/app/src

      # Anonymous volume (protect node_modules)
      - /app/node_modules

volumes:
  app-data:   # Declare named volumes
```

### Dependencies

```yaml
services:
  web:
    depends_on:
      - db
      - redis

    # With health check condition (Compose v2)
    depends_on:
      db:
        condition: service_healthy
```

### Health Checks

```yaml
services:
  db:
    image: mysql:8.0
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

### Restart Policy

```yaml
services:
  web:
    restart: always          # Always restart
    restart: unless-stopped  # Restart unless manually stopped
    restart: on-failure      # Restart only on failure
    restart: "no"            # Never restart (default)
```

### Resource Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          memory: 256M
```

---

## Networks

```yaml
services:
  web:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend

networks:
  frontend:
  backend:
```

By default, Compose creates a single network for all services. Custom networks let you isolate groups of services.

---

## Common Patterns

### Web App + Database

```yaml
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### Development Override

```yaml
# docker-compose.yml (base)
services:
  web:
    build: .
    ports:
      - "3000:3000"

# docker-compose.override.yml (dev, auto-loaded)
services:
  web:
    volumes:
      - ./src:/app/src
    environment:
      NODE_ENV: development
    command: npx nodemon src/index.js
```

### Multiple Databases

```yaml
services:
  app:
    build: .
    depends_on:
      - mysql
      - redis

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - mysql-data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  mysql-data:
  redis-data:
```

---

## Variable Substitution

```yaml
services:
  web:
    image: myapp:${TAG:-latest}       # Default to "latest"
    ports:
      - "${PORT:-3000}:3000"          # Default to 3000

# Set variables in .env file or shell:
# TAG=1.0 PORT=8080 docker compose up
```

---

## Useful Flags

| Flag | Command | Purpose |
|------|---------|---------|
| `-d` | `up -d` | Detached mode (background) |
| `--build` | `up --build` | Rebuild images before starting |
| `-v` | `down -v` | Remove volumes when stopping |
| `--force-recreate` | `up --force-recreate` | Recreate containers even if unchanged |
| `--no-deps` | `up --no-deps web` | Start service without dependencies |
| `--scale` | `up --scale web=3` | Run multiple instances |
| `--profile` | `up --profile debug` | Start services matching profile |

---

**[Back to Workshop Home](../../README.md)**
