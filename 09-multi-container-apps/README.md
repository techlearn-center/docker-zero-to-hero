# Module 09 — Multi-Container Apps (15 pts)

> **"One container, one job."** In this module, you'll run your app and a MySQL database in separate containers connected through a Docker network.

---

## What You'll Learn

- Why you should run each service in its own container
- How Docker networking works
- How to create and use a Docker network
- How to run MySQL in a container
- How to connect your app to a MySQL database

---

## Why Multi-Container?

Up to now, our app uses SQLite — a file-based database bundled inside the container. That works for learning, but in production you'd use a proper database server.

```
SINGLE CONTAINER (current):         MULTI-CONTAINER (this module):

┌────────────────────┐              ┌──────────┐   ┌──────────┐
│  Node.js App       │              │ Node.js  │   │  MySQL   │
│  + SQLite DB       │              │ App      │←→│  Server  │
│  (everything       │              │          │   │          │
│   in one box)      │              │ Port 3000│   │ Port 3306│
└────────────────────┘              └──────────┘   └──────────┘

❌ DB scales with app               ✅ Scale independently
❌ Single point of failure          ✅ Replace parts separately
❌ Hard to maintain                 ✅ Clean separation
```

### The "One Container, One Job" Rule

Each container should do **one thing well**:
- Web server → one container
- Database → one container
- Cache → one container
- Queue → one container

---

## Step 1 — Create a Docker Network

Containers need to be on the same network to talk to each other:

```bash
docker network create todo-network
```

Verify:

```bash
docker network ls
```

### How Networks Work

```
┌─── Docker Network: todo-network ───────────────────┐
│                                                     │
│  ┌──────────┐         ┌──────────┐                 │
│  │ todo-app │───DNS──→│  mysql   │                 │
│  │          │         │          │                 │
│  │ "mysql"  │         │ Port 3306│                 │
│  └──────────┘         └──────────┘                 │
│                                                     │
│  Containers on the same network can find each      │
│  other by NAME (Docker provides built-in DNS)      │
└─────────────────────────────────────────────────────┘
```

Key insight: **Containers on the same Docker network can reach each other using the container name as the hostname.**

---

## Step 2 — Start MySQL

```bash
docker run -d \
  --name mysql \
  --network todo-network \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  -v todo-mysql-data:/var/lib/mysql \
  mysql:8.0
```

| Flag | Purpose |
|------|---------|
| `--name mysql` | Name the container "mysql" (used as hostname on the network) |
| `--network todo-network` | Connect to our network |
| `-e MYSQL_ROOT_PASSWORD=secret` | Set the root password |
| `-e MYSQL_DATABASE=todos` | Create a database named "todos" |
| `-v todo-mysql-data:/var/lib/mysql` | Persist MySQL data |
| `mysql:8.0` | Use MySQL 8.0 image |

Wait a few seconds for MySQL to initialize, then verify:

```bash
docker logs mysql
```

Look for: `ready for connections` in the output.

---

## Step 3 — Connect Your App to MySQL

Stop any existing todo-app containers:

```bash
docker rm -f $(docker ps -q --filter ancestor=todo-app)
```

Now run the app with MySQL connection settings:

```bash
docker run -dp 3000:3000 \
  --name todo-app \
  --network todo-network \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  todo-app
```

| Flag | Purpose |
|------|---------|
| `--network todo-network` | Same network as MySQL |
| `-e MYSQL_HOST=mysql` | Hostname = MySQL container name |
| `-e MYSQL_USER=root` | MySQL username |
| `-e MYSQL_PASSWORD=secret` | MySQL password (matches what we set) |
| `-e MYSQL_DB=todos` | Database name (matches what we created) |

### How the App Switches to MySQL

The app detects `MYSQL_HOST` and switches from SQLite to MySQL automatically:

```
┌─────────────────────────────────────────────┐
│  src/routes/todos.js                        │
│                                             │
│  if (process.env.MYSQL_HOST) {              │
│      persistence = require('../persistence/ │
│                              mysql');        │
│  } else {                                   │
│      persistence = require('../persistence/ │
│                              sqlite');       │
│  }                                          │
└─────────────────────────────────────────────┘
```

---

## Step 4 — Verify It Works

1. Open http://localhost:3000
2. Add some todos
3. Check the app logs:
   ```bash
   docker logs todo-app
   ```
   You should see: `Using MySQL persistence`

4. **Prove multi-container works** — restart just the app:
   ```bash
   docker rm -f todo-app
   docker run -dp 3000:3000 \
     --name todo-app \
     --network todo-network \
     -e MYSQL_HOST=mysql \
     -e MYSQL_USER=root \
     -e MYSQL_PASSWORD=secret \
     -e MYSQL_DB=todos \
     todo-app
   ```
   Your todos are still there! They're in MySQL, not the app container.

---

## Step 5 — Explore the Network

```bash
# List networks
docker network ls

# Inspect the network (see connected containers)
docker network inspect todo-network

# Test connectivity from inside a container
docker exec todo-app ping -c 2 mysql
```

### DNS Resolution in Action

```bash
# From inside the app container, "mysql" resolves to the MySQL container's IP
docker exec todo-app nslookup mysql
```

---

## The Full Picture

```
  Host Machine
  ┌──────────────────────────────────────────────┐
  │                                              │
  │   Browser ──→ localhost:3000                 │
  │                    │                         │
  │   ┌── todo-network ┼────────────────────┐    │
  │   │                │                    │    │
  │   │   ┌────────────┴───┐  ┌──────────┐ │    │
  │   │   │   todo-app     │  │  mysql   │ │    │
  │   │   │   :3000        │─→│  :3306   │ │    │
  │   │   │                │  │          │ │    │
  │   │   └────────────────┘  └────┬─────┘ │    │
  │   │                            │       │    │
  │   └────────────────────────────┼───────┘    │
  │                                │            │
  │                     ┌──────────┴─────┐      │
  │                     │ todo-mysql-data │      │
  │                     │   (volume)     │      │
  │                     └────────────────┘      │
  └──────────────────────────────────────────────┘
```

---

## Progressive Hints

<details>
<summary>💡 Hint 1 — The 3 pieces you need</summary>

1. A Docker **network** for container communication
2. A **MySQL** container on that network
3. Your **app** container on that network with environment variables

</details>

<details>
<summary>💡 Hint 2 — The environment variables</summary>

The app needs these env vars to connect to MySQL:
- `MYSQL_HOST` — the MySQL container's name (e.g., "mysql")
- `MYSQL_USER` — MySQL username (e.g., "root")
- `MYSQL_PASSWORD` — MySQL password (must match MySQL container)
- `MYSQL_DB` — Database name (must match MySQL container)

</details>

<details>
<summary>💡 Hint 3 — Complete setup commands</summary>

```bash
# 1. Create network
docker network create todo-network

# 2. Start MySQL
docker run -d \
  --name mysql \
  --network todo-network \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  -v todo-mysql-data:/var/lib/mysql \
  mysql:8.0

# 3. Start app
docker run -dp 3000:3000 \
  --name todo-app \
  --network todo-network \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  todo-app
```

</details>

---

## Grading Criteria (15 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Docker network exists | 3 | A custom network was created |
| MySQL container running | 4 | MySQL container on the network with correct env vars |
| App connected to MySQL | 4 | App container on the same network with MYSQL_HOST set |
| Environment variables set | 4 | MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB are configured |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You created a Docker network
- [ ] MySQL is running in its own container on the network
- [ ] The app connects to MySQL (check logs for "Using MySQL persistence")
- [ ] Todos persist when you restart the app container (but not MySQL)
- [ ] `python run.py --module 09` scores 15/15

---

**Next up:** [Module 10 — Use Docker Compose](../10-use-docker-compose/README.md) — Simplify all of this into a single YAML file!
