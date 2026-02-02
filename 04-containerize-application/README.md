# Module 04 — Containerize the Application (25 pts)

> **"Your app runs on your machine. Let's make it run on EVERY machine."** In this module, you'll write a Dockerfile, build your first image, and run the todo app in a container.

---

## What You'll Learn

- How to write a Dockerfile from scratch
- How to build a Docker image
- How to run a container and access it from your browser
- How Docker layer caching works in practice

---

## Step 1 — Understand the Dockerfile

A Dockerfile is a recipe — a series of instructions that tells Docker how to build an image.

Here are the instructions you'll use:

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Set the base image | `FROM node:18-alpine` |
| `WORKDIR` | Set the working directory inside the container | `WORKDIR /app` |
| `COPY` | Copy files from your machine into the image | `COPY package.json .` |
| `RUN` | Execute a command during the build | `RUN npm install --production` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 3000` |
| `CMD` | Define the default command to run | `CMD ["node", "src/index.js"]` |

### How It Maps to Our App

```
Your Machine                          Docker Image
┌──────────────────┐                 ┌──────────────────┐
│ app/             │                 │ /app/            │
│ ├── package.json │  ── COPY ──→   │ ├── package.json │
│ ├── src/         │                 │ ├── node_modules/│ ← npm install
│ │   ├── index.js │  ── COPY ──→   │ ├── src/         │
│ │   └── ...      │                 │ │   ├── index.js │
│ └── spec/        │                 │ │   └── ...      │
└──────────────────┘                 └──────────────────┘
```

---

## Step 2 — Write Your Dockerfile

Open `app/Dockerfile` in your editor. You'll see a starter template with TODOs.

Your task: **Complete the Dockerfile** with these 7 instructions (in order):

1. **FROM** — Use `node:18-alpine` as the base image
2. **WORKDIR** — Set working directory to `/app`
3. **COPY** — Copy `package.json` (and `package-lock.json` or `yarn.lock` if present)
4. **RUN** — Install production dependencies with `npm install --production`
5. **COPY** — Copy everything else (`. .`)
6. **EXPOSE** — Document port `3000`
7. **CMD** — Start the app with `node src/index.js`

### Why Copy package.json First?

```
BAD (slow rebuilds):              GOOD (fast rebuilds):
┌──────────────────┐              ┌──────────────────┐
│ COPY . .         │ ← Every      │ COPY package* .  │ ← Only if
│ RUN npm install  │   change     │ RUN npm install  │   deps change
│                  │   reinstalls │ COPY . .         │
└──────────────────┘              └──────────────────┘

Changed a comment in index.js?     Changed a comment in index.js?
→ npm install runs again (slow)    → npm install is cached! (fast)
```

---

### Progressive Hints

<details>
<summary>💡 Hint 1 — The structure</summary>

Your Dockerfile should have exactly 7 lines of instructions (not counting comments):

```dockerfile
FROM ...
WORKDIR ...
COPY ...
RUN ...
COPY ...
EXPOSE ...
CMD ...
```

</details>

<details>
<summary>💡 Hint 2 — Key details</summary>

- Base image: `node:18-alpine` (small, production-ready)
- Working directory: `/app`
- Copy `package.json` first (just this file, for layer caching)
- Install with `npm install --production` (skip devDependencies)
- Then copy everything: `COPY . .`
- Expose port `3000`
- CMD uses exec form: `CMD ["node", "src/index.js"]`

</details>

<details>
<summary>💡 Hint 3 — Full solution</summary>

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```

</details>

---

## Step 3 — Build the Image

From the `app/` directory, run:

```bash
cd app
docker build -t todo-app .
```

Let's break this down:

| Part | Meaning |
|------|---------|
| `docker build` | Build an image from a Dockerfile |
| `-t todo-app` | Tag (name) the image as "todo-app" |
| `.` | Use the current directory as the build context |

You should see output like:

```
[+] Building 23.4s (10/10) FINISHED
 => [1/5] FROM node:18-alpine
 => [2/5] WORKDIR /app
 => [3/5] COPY package.json .
 => [4/5] RUN npm install --production
 => [5/5] COPY . .
 => exporting to image
 => => naming to docker.io/library/todo-app
```

### Verify the image was created:

```bash
docker images | grep todo-app
```

Expected output:

```
todo-app   latest   abc123def456   10 seconds ago   180MB
```

---

## Step 4 — Run the Container

```bash
docker run -dp 3000:3000 todo-app
```

| Flag | Meaning |
|------|---------|
| `-d` | Run in **detached** mode (background) |
| `-p 3000:3000` | Map port 3000 on your machine to port 3000 in the container |

### Port Mapping Explained

```
Your Machine                    Container
┌──────────────────┐           ┌──────────────────┐
│                  │           │                  │
│   Browser        │           │   Node.js App    │
│   localhost:3000 │──────────→│   :3000          │
│                  │  -p 3000  │                  │
│                  │   :3000   │                  │
└──────────────────┘           └──────────────────┘
```

### Open in Your Browser

Navigate to: **http://localhost:3000**

You should see the todo app! Try adding a few todos to make sure it works.

### Verify the Container is Running

```bash
docker ps
```

Expected output:

```
CONTAINER ID   IMAGE      COMMAND                  STATUS         PORTS
a1b2c3d4e5f6   todo-app   "node src/index.js"      Up 2 minutes   0.0.0.0:3000->3000/tcp
```

---

## Step 5 — Explore Useful Commands

Now that your container is running, try these commands:

```bash
# View container logs
docker logs <container-id>

# View logs in real-time
docker logs -f <container-id>

# List all containers (including stopped)
docker ps -a

# Stop the container
docker stop <container-id>

# Remove the container
docker rm <container-id>

# Stop AND remove in one command
docker rm -f <container-id>
```

**Tip:** You only need the first few characters of the container ID:

```bash
docker stop a1b2    # Works! Docker matches the prefix
```

---

## What Just Happened?

Let's recap the entire flow:

```
  1. You wrote a Dockerfile          (recipe)
  2. docker build created an image   (lunchbox)
  3. docker run started a container  (eating lunch)
  4. -p mapped the port              (opening the lid)
  5. Browser accessed the app        (enjoying the meal!)

  ┌────────────┐    build    ┌────────────┐    run    ┌────────────┐
  │ Dockerfile │ ──────────→ │   Image    │ ────────→ │ Container  │
  │            │             │  todo-app  │           │  :3000     │
  └────────────┘             └────────────┘           └────────────┘
```

---

## Grading Criteria (25 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| FROM instruction | 3 | Uses `node:18-alpine` (or similar Node base) |
| WORKDIR instruction | 3 | Sets working directory to `/app` |
| COPY package.json | 4 | Copies package.json before install (layer caching) |
| RUN npm install | 4 | Installs dependencies |
| COPY source code | 3 | Copies remaining source files |
| EXPOSE instruction | 3 | Documents port 3000 |
| CMD instruction | 3 | Defines start command |
| Image builds | 2 | `docker build` succeeds without errors |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] Your `app/Dockerfile` has all 7 instructions
- [ ] `docker build -t todo-app .` completes successfully
- [ ] `docker run -dp 3000:3000 todo-app` starts the container
- [ ] The app is accessible at http://localhost:3000
- [ ] `python run.py --module 04` scores 25/25

---

**Next up:** [Module 05 — Update the Application](../05-update-application/README.md) — Change the code and see how Docker handles updates.
