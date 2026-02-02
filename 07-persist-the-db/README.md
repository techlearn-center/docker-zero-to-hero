# Module 07 — Persist the DB (10 pts)

> **"Containers are like sticky notes — great for quick work, but terrible for permanent records."** In this module, you'll use Docker volumes to persist your todo data across container restarts.

---

## What You'll Learn

- Why container data is lost when containers are removed
- What Docker volumes are and how they work
- How to create and use named volumes
- How to inspect volume data

---

## The Problem: Ephemeral Containers

Remember Module 05? When we removed the container, all todos were gone. Here's why:

```
Container Filesystem (ephemeral)
┌─────────────────────────────────┐
│  /app/                          │
│  /app/src/                      │
│  /app/data/todos.db  ← SQLite  │  ← LIVES INSIDE THE CONTAINER
│  /etc/                          │
│  /usr/                          │
└────────────────┬────────────────┘
                 │
          docker rm -f
                 │
                 ↓
            💨 GONE
```

Each container has its own **writable layer** on top of the read-only image layers. When the container is removed, that writable layer is deleted.

---

## The Solution: Volumes

A **volume** is a persistent storage area that lives **outside** the container:

```
Container                        Host Machine
┌──────────────────┐            ┌──────────────────┐
│  /app/            │            │                  │
│  /app/data/ ──────┼──mount──→ │  /var/lib/docker │
│  (todos.db)       │            │  /volumes/       │
│                  │            │  todo-db/_data/  │
└──────────────────┘            │  todos.db        │
                                │                  │
 Container removed?             │  DATA SURVIVES!  │
 No problem!                    └──────────────────┘
```

---

## Step 1 — Create a Named Volume

```bash
docker volume create todo-db
```

Verify it was created:

```bash
docker volume ls
```

Expected output:

```
DRIVER    VOLUME NAME
local     todo-db
```

---

## Step 2 — Run with the Volume Mounted

Stop any existing todo-app container first:

```bash
docker rm -f $(docker ps -q --filter ancestor=todo-app)
```

Now run with the volume:

```bash
docker run -dp 3000:3000 -v todo-db:/app/data todo-app
```

| Flag | Meaning |
|------|---------|
| `-v todo-db:/app/data` | Mount the `todo-db` volume at `/app/data` inside the container |

### How the Mount Works

```
  -v  todo-db  :  /app/data
      ───┬───     ────┬─────
         │            │
   Volume name    Mount point inside
   (on host)      the container

   The SQLite database (todos.db) gets stored in
   /app/data/ → which is actually the todo-db volume
   → which persists on the host machine
```

---

## Step 3 — Test Persistence

1. Open http://localhost:3000
2. Add a few todos (e.g., "Learn Docker volumes", "Persist data")
3. Stop and remove the container:
   ```bash
   docker rm -f $(docker ps -q --filter ancestor=todo-app)
   ```
4. Start a **new** container with the same volume:
   ```bash
   docker run -dp 3000:3000 -v todo-db:/app/data todo-app
   ```
5. Open http://localhost:3000 again

**Your todos are still there!** The data survived because it's stored in the volume, not the container.

---

## Step 4 — Inspect the Volume

```bash
docker volume inspect todo-db
```

Output:

```json
[
    {
        "CreatedAt": "2024-01-15T10:30:00Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/todo-db/_data",
        "Name": "todo-db",
        "Options": {},
        "Scope": "local"
    }
]
```

The `Mountpoint` shows where the data actually lives on your host machine.

---

## Types of Mounts

Docker has three types of mounts:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. VOLUMES (recommended)                               │
│     docker run -v my-volume:/app/data ...               │
│     → Managed by Docker, stored in Docker's area        │
│     → Best for: persistent data (databases, uploads)    │
│                                                         │
│  2. BIND MOUNTS (Module 08)                             │
│     docker run -v /host/path:/container/path ...        │
│     → Maps a specific host directory                    │
│     → Best for: development (live code reloading)       │
│                                                         │
│  3. TMPFS MOUNTS                                        │
│     docker run --tmpfs /app/tmp ...                     │
│     → Stored in memory only                             │
│     → Best for: sensitive data, temporary files         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

In this module, we use **volumes**. In the next module, we'll use **bind mounts**.

---

## Volume Lifecycle Commands

```bash
# Create a volume
docker volume create my-volume

# List all volumes
docker volume ls

# Inspect a volume
docker volume inspect my-volume

# Remove a volume
docker volume rm my-volume

# Remove all unused volumes (careful!)
docker volume prune
```

---

## Progressive Hints

<details>
<summary>💡 Hint 1 — The key flag</summary>

The flag is `-v VOLUME_NAME:MOUNT_PATH`. The mount path should be where your app stores its database.

</details>

<details>
<summary>💡 Hint 2 — Where does SQLite store data?</summary>

Look at `app/src/persistence/sqlite.js` — the database path defaults to `../../data/todos.db` relative to the script, which resolves to `/app/data/todos.db` inside the container.

So mount your volume at `/app/data`.

</details>

<details>
<summary>💡 Hint 3 — Full commands</summary>

```bash
# Create the volume
docker volume create todo-db

# Stop old container
docker rm -f $(docker ps -q --filter ancestor=todo-app)

# Run with volume
docker run -dp 3000:3000 -v todo-db:/app/data todo-app
```

</details>

---

## Grading Criteria (10 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Volume created | 5 | A named volume exists (e.g., `todo-db`) |
| Volume mount configured | 5 | Container runs with `-v` flag mounting to `/app/data` |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You created a named volume: `docker volume create todo-db`
- [ ] You ran the container with the volume: `-v todo-db:/app/data`
- [ ] Todos persist after stopping and restarting the container
- [ ] `docker volume inspect todo-db` shows the volume details
- [ ] `python run.py --module 07` scores 10/10

---

**Next up:** [Module 08 — Use Bind Mounts](../08-use-bind-mounts/README.md) — Speed up development with live code reloading.
