# Module 10 — Use Docker Compose (15 pts)

> **"That was a lot of commands in Module 09. What if one file could replace them all?"** In this module, you'll define your entire multi-container application in a single `docker-compose.yml` file.

---

## What You'll Learn

- What Docker Compose is and why it exists
- How to write a `docker-compose.yml` file
- How to start/stop multi-container apps with one command
- How Compose handles networks, volumes, and environment variables

---

## The Problem: Too Many Commands

In Module 09, you ran something like this:

```bash
docker network create todo-network
docker run -d --name mysql --network todo-network -e MYSQL_ROOT_PASSWORD=secret ...
docker run -dp 3000:3000 --name todo-app --network todo-network -e MYSQL_HOST=mysql ...
```

That's a lot to remember and type every time. Now imagine a real app with 5-10 services...

**Docker Compose** lets you define all of this in a single YAML file:

```
 Without Compose:                  With Compose:

 $ docker network create ...       $ docker compose up
 $ docker run ... mysql ...
 $ docker run ... app ...          That's it. One command.
 $ docker run ... redis ...
 $ docker run ... nginx ...
```

---

## Step 1 — Understand the Structure

A `docker-compose.yml` file has three main sections:

```yaml
services:        # Define your containers
  web:           # Service 1
    ...
  mysql:         # Service 2
    ...

volumes:         # Define named volumes
  mysql-data:
```

Each **service** becomes a container. Compose automatically:
- Creates a **network** for all services (they can reach each other by service name)
- Manages **container lifecycle** (start, stop, restart)
- Handles **dependencies** between services

---

## Step 2 — Write Your docker-compose.yml

Open the `docker-compose.yml` file in the project root. You'll see a starter template with TODOs.

Your task: **Define two services and a volume.**

### Service 1: web (the Node.js app)

| Property | Value |
|----------|-------|
| `build` | `./app` |
| `ports` | `3000:3000` |
| `environment` | `MYSQL_HOST: mysql`, `MYSQL_USER: root`, `MYSQL_PASSWORD: secret`, `MYSQL_DB: todos` |
| `depends_on` | `mysql` |

### Service 2: mysql (the database)

| Property | Value |
|----------|-------|
| `image` | `mysql:8.0` |
| `environment` | `MYSQL_ROOT_PASSWORD: secret`, `MYSQL_DATABASE: todos` |
| `volumes` | `mysql-data:/var/lib/mysql` |

### Volume: mysql-data

A named volume to persist MySQL data.

---

## Step 3 — Complete the File

### Progressive Hints

<details>
<summary>💡 Hint 1 — The skeleton</summary>

```yaml
services:
  web:
    build: ...
    ports:
      - ...
    environment:
      ...
    depends_on:
      - ...

  mysql:
    image: ...
    environment:
      ...
    volumes:
      - ...

volumes:
  ...:
```

</details>

<details>
<summary>💡 Hint 2 — Key values</summary>

- `build: ./app` tells Compose to build from the `app/` directory
- `ports: - "3000:3000"` maps the port
- Environment variables can use `KEY: value` format under `environment:`
- `depends_on` ensures MySQL starts before the app
- Volume format: `volume-name:/path/in/container`

</details>

<details>
<summary>💡 Hint 3 — Complete solution</summary>

```yaml
services:
  web:
    build: ./app
    ports:
      - "3000:3000"
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

</details>

---

## Step 4 — Start the Application

First, stop all running containers from previous modules:

```bash
docker rm -f $(docker ps -aq)
```

Now start everything with Compose:

```bash
docker compose up -d
```

| Flag | Meaning |
|------|---------|
| `up` | Create and start all services |
| `-d` | Detached mode (background) |

You'll see:

```
[+] Running 3/3
 ✔ Network docker-zero-to-hero_default  Created
 ✔ Container docker-zero-to-hero-mysql-1  Started
 ✔ Container docker-zero-to-hero-web-1    Started
```

Notice: **Compose creates a network automatically!** No need for `docker network create`.

---

## Step 5 — Verify

Open http://localhost:3000 — the app should be running!

Check the logs:

```bash
docker compose logs
```

Or follow logs in real-time:

```bash
docker compose logs -f
```

Check specific service logs:

```bash
docker compose logs web
docker compose logs mysql
```

---

## Step 6 — Compose Commands

```bash
# Start all services
docker compose up -d

# Stop all services (preserves volumes)
docker compose down

# Stop and remove volumes too
docker compose down -v

# View running services
docker compose ps

# View logs
docker compose logs

# Rebuild images (after code changes)
docker compose up -d --build

# Restart a specific service
docker compose restart web
```

### Lifecycle Comparison

```
  docker compose up -d        docker compose down
  ┌──────────────────┐        ┌──────────────────┐
  │ Creates:         │        │ Removes:         │
  │  ✓ Network       │        │  ✓ Containers    │
  │  ✓ Volumes       │        │  ✓ Network       │
  │  ✓ Containers    │        │  ✗ Volumes       │
  │  ✓ Starts all    │        │    (preserved!)  │
  └──────────────────┘        └──────────────────┘

  docker compose down -v
  ┌──────────────────┐
  │ Removes:         │
  │  ✓ Containers    │
  │  ✓ Network       │
  │  ✓ Volumes       │  ← Data lost!
  └──────────────────┘
```

---

## Understanding depends_on

```yaml
services:
  web:
    depends_on:
      - mysql    # MySQL starts BEFORE web
```

```
Start order:  mysql → web
Stop order:   web → mysql (reverse)
```

**Important:** `depends_on` only waits for the container to **start**, not for the service to be **ready**. MySQL might take a few seconds to initialize. In production, you'd add a healthcheck or retry logic.

---

## The Full Picture with Compose

```
  docker-compose.yml
  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │  services:                                       │
  │    web:  ──→  ┌──────────┐                       │
  │               │ todo-app │ ←── build: ./app      │
  │               │ :3000    │                       │
  │               └─────┬────┘                       │
  │                     │ MYSQL_HOST=mysql            │
  │    mysql: →  ┌──────┴────┐                       │
  │              │  MySQL   │ ←── image: mysql:8.0   │
  │              │  :3306   │                        │
  │              └─────┬────┘                        │
  │                    │                             │
  │  volumes:          │                             │
  │    mysql-data: ──→ │ /var/lib/mysql              │
  │                                                  │
  │  network: (auto-created)                         │
  │                                                  │
  └──────────────────────────────────────────────────┘
```

---

## Grading Criteria (15 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Web service defined | 3 | `services.web` with build context |
| Port mapping | 2 | Port 3000 mapped |
| MySQL service defined | 3 | `services.mysql` with image |
| Environment variables | 3 | MySQL connection vars on web service |
| Volume defined | 2 | Named volume for MySQL data |
| depends_on | 2 | Web depends on mysql |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] Your `docker-compose.yml` defines both `web` and `mysql` services
- [ ] `docker compose up -d` starts both services
- [ ] The app is accessible at http://localhost:3000
- [ ] `docker compose logs web` shows "Using MySQL persistence"
- [ ] `docker compose down` stops everything cleanly
- [ ] `python run.py --module 10` scores 15/15

---

**Next up:** [Module 11 — Image Building Best Practices](../11-image-building-best-practices/README.md) — Optimize your Docker images for production.
