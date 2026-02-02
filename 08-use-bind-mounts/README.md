# Module 08 — Use Bind Mounts (10 pts)

> **"Volumes persist data. Bind mounts connect worlds."** In this module, you'll use bind mounts to create a development workflow where code changes are reflected instantly — no rebuild needed.

---

## What You'll Learn

- The difference between volumes and bind mounts
- How to use bind mounts for development
- How to set up live-reloading with nodemon
- When to use volumes vs bind mounts

---

## Volumes vs Bind Mounts

```
VOLUMES                              BIND MOUNTS
┌──────────────────┐                ┌──────────────────┐
│   Container      │                │   Container      │
│   /app/data/ ────┼──→ Docker      │   /app/ ─────────┼──→ Your actual
│                  │    managed     │                  │    project folder
│                  │    storage     │                  │    on disk
└──────────────────┘                └──────────────────┘

  ✅ Persist data                    ✅ Live code changes
  ✅ Docker manages location         ✅ You control the path
  ✅ Best for: databases             ✅ Best for: development
  ❌ Can't easily edit files         ❌ Not for production
```

---

## Step 1 — Understand the Dev Workflow Problem

Without bind mounts, every code change requires:

```
Edit code → docker build → docker rm → docker run → refresh browser

  ~30 seconds per change 😫
```

With bind mounts:

```
Edit code → refresh browser

  Instant! 🚀
```

---

## Step 2 — Run with a Bind Mount

Stop any running todo-app containers first:

```bash
docker rm -f $(docker ps -q --filter ancestor=todo-app)
```

Now run with a bind mount that maps your local `app/` directory into the container:

```bash
docker run -dp 3000:3000 \
  -v todo-db:/app/data \
  -v "$(pwd)/app:/app" \
  -v /app/node_modules \
  -w /app \
  todo-app sh -c "npm install && npx nodemon src/index.js"
```

> **On Windows (PowerShell):**
> ```powershell
> docker run -dp 3000:3000 `
>   -v todo-db:/app/data `
>   -v "${PWD}/app:/app" `
>   -v /app/node_modules `
>   -w /app `
>   todo-app sh -c "npm install && npx nodemon src/index.js"
> ```

Let's break down every flag:

| Flag | Purpose |
|------|---------|
| `-v todo-db:/app/data` | Named volume for database persistence (from Module 07) |
| `-v "$(pwd)/app:/app"` | **Bind mount:** your local `app/` → container's `/app/` |
| `-v /app/node_modules` | Anonymous volume to prevent overwriting `node_modules` |
| `-w /app` | Set working directory to `/app` |
| `sh -c "npm install && npx nodemon src/index.js"` | Install deps and start with nodemon (auto-restart on file changes) |

### The node_modules Trick

```
Without -v /app/node_modules:

  Host: app/               Container: /app/
  ├── package.json         ├── package.json
  ├── src/                 ├── src/
  └── (no node_modules)    └── (no node_modules!)  ← Bind mount
                                                      overwrites everything!

With -v /app/node_modules:

  Host: app/               Container: /app/
  ├── package.json         ├── package.json
  ├── src/                 ├── src/
  └── (no node_modules)    └── node_modules/  ← Anonymous volume
                                                 preserves this!
```

---

## Step 3 — Test Live Reloading

1. Open http://localhost:3000
2. Open `app/src/static/index.html` in your editor
3. Change the `<h1>` text:

   ```html
   <h1>Todo App - Live Reload!</h1>
   ```

4. Save the file
5. Watch the Docker logs:

   ```bash
   docker logs -f $(docker ps -q --filter ancestor=todo-app)
   ```

   You should see nodemon restart:
   ```
   [nodemon] restarting due to changes...
   [nodemon] starting `node src/index.js`
   Server running on port 3000
   ```

6. Refresh http://localhost:3000 — the change is there instantly!

---

## Step 4 — Understand the Flow

```
  Your Editor                Container                Browser
  ┌──────────┐    bind      ┌──────────┐    port    ┌──────────┐
  │  Edit    │───mount────→ │ nodemon  │───3000───→ │ See the  │
  │  file    │   syncs      │ detects  │   maps     │ change!  │
  │          │   instantly  │ restarts │            │          │
  └──────────┘              └──────────┘            └──────────┘
```

**No rebuild needed!** The bind mount keeps the container in sync with your host filesystem. Nodemon watches for changes and restarts the server automatically.

---

## When to Use Which

| Scenario | Use | Why |
|----------|-----|-----|
| Database files | **Volume** | Managed by Docker, persists data |
| Development code | **Bind mount** | Live editing, no rebuilds |
| Production | **Volume** (or none) | Don't expose host filesystem |
| Config files | **Bind mount** | Easy to edit outside container |
| Temporary data | **tmpfs** | Fast, stored in memory |

---

## Progressive Hints

<details>
<summary>💡 Hint 1 — The key difference</summary>

Bind mounts use an **absolute host path** instead of a volume name:

```
-v /absolute/path/on/host:/path/in/container    ← Bind mount
-v volume-name:/path/in/container               ← Named volume
```

</details>

<details>
<summary>💡 Hint 2 — Getting the right path</summary>

Use `$(pwd)` (Linux/Mac) or `${PWD}` (PowerShell) to get the current directory. Make sure you're in the project root (not inside `app/`):

```bash
# From project root:
-v "$(pwd)/app:/app"
```

</details>

<details>
<summary>💡 Hint 3 — Full dev command</summary>

```bash
# Make sure you're in the project root directory
docker run -dp 3000:3000 \
  -v todo-db:/app/data \
  -v "$(pwd)/app:/app" \
  -v /app/node_modules \
  -w /app \
  todo-app sh -c "npm install && npx nodemon src/index.js"
```

</details>

---

## Grading Criteria (10 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Bind mount concept | 5 | Understanding of bind mount flag syntax |
| Dev workflow configured | 5 | Container run command includes bind mount for source code |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You ran the container with a bind mount (`-v "$(pwd)/app:/app"`)
- [ ] You edited a file and saw the change without rebuilding
- [ ] You understand the difference between volumes and bind mounts
- [ ] You know why the anonymous volume for `node_modules` is needed
- [ ] `python run.py --module 08` scores 10/10

---

**Next up:** [Module 09 — Multi-Container Apps](../09-multi-container-apps/README.md) — Connect your app to a MySQL database running in another container.
