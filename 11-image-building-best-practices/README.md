# Module 11 — Image Building Best Practices (5 pts)

> **"A 1GB image works. A 50MB image works better."** In this module, you'll learn how to build smaller, faster, more secure Docker images using multi-stage builds and other best practices.

---

## What You'll Learn

- How to use multi-stage builds to reduce image size
- How `.dockerignore` works and why it matters
- Layer ordering strategies for faster builds
- Security best practices for Docker images

---

## Problem: Image Size Matters

Let's check our current image size:

```bash
docker images todo-app
```

You might see something like:

```
REPOSITORY   TAG       SIZE
todo-app     latest    180MB
```

180MB for a simple todo app? We can do much better.

```
Why Image Size Matters:
┌─────────────────────────────────────────────┐
│                                             │
│  📦 Smaller image = faster pulls            │
│  🚀 Smaller image = faster deployments      │
│  🔒 Smaller image = less attack surface     │
│  💰 Smaller image = less storage costs      │
│  📡 Smaller image = less bandwidth          │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Strategy 1: Multi-Stage Builds

A multi-stage build uses multiple `FROM` statements. Each stage can use a different base image, and you only copy what you need to the final image.

### Before (Single Stage)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install           # Installs ALL deps (including devDeps)
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```

The problem: the final image contains:
- npm cache
- devDependencies (test tools, etc.)
- Build artifacts you don't need at runtime

### After (Multi-Stage)

Create a file called `app/Dockerfile.multistage`:

```dockerfile
# ---- Stage 1: Build ----
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json .
RUN npm install

# ---- Stage 2: Production ----
FROM node:18-alpine AS production
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY --from=build /app/node_modules ./node_modules_full
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```

Or more simply for our Node.js app:

```dockerfile
# ---- Stage 1: Install all deps (for testing/building) ----
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json .
RUN npm install

# ---- Stage 2: Production image ----
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```

### How Multi-Stage Works

```
Stage 1 (deps):                    Stage 2 (production):
┌──────────────────┐              ┌──────────────────┐
│ node:18-alpine   │              │ node:18-alpine   │
│ ALL node_modules │──copy what──→│ PROD node_modules│
│ dev dependencies │  you need    │ app source only  │
│ test tools       │              │                  │
│ build artifacts  │              │ SMALLER IMAGE!   │
│ ~180MB           │              │ ~120MB           │
└──────────────────┘              └──────────────────┘

Stage 1 is DISCARDED              Stage 2 is the FINAL image
```

### Build and Compare

```bash
cd app

# Build the multi-stage version
docker build -f Dockerfile.multistage -t todo-app:multistage .

# Compare sizes
docker images | grep todo-app
```

---

## Strategy 2: .dockerignore

Create a file called `app/.dockerignore`:

```
node_modules
.git
.gitignore
*.md
.env
.DS_Store
npm-debug.log
spec/
```

### Before vs After .dockerignore

```
WITHOUT .dockerignore:              WITH .dockerignore:

Build context sent to Docker:       Build context sent to Docker:
├── node_modules/ (150MB!)          ├── package.json
├── .git/ (10MB)                    ├── src/
├── package.json                    └── (that's it!)
├── src/
├── spec/                           ~50KB vs ~160MB
├── README.md
└── ...

Build time: 30 seconds             Build time: 3 seconds
```

---

## Strategy 3: Layer Ordering

Order your Dockerfile instructions from **least frequently changed** to **most frequently changed**:

```dockerfile
# ✅ GOOD: Optimal layer ordering
FROM node:18-alpine            # Almost never changes
WORKDIR /app                   # Almost never changes
COPY package.json .            # Changes when deps change
RUN npm install --production   # Runs only when package.json changes
COPY . .                       # Changes every code edit
CMD ["node", "src/index.js"]   # Almost never changes
```

```dockerfile
# ❌ BAD: Every code change reinstalls deps
FROM node:18-alpine
WORKDIR /app
COPY . .                       # Changes every code edit
RUN npm install --production   # Runs EVERY TIME (layer above changed)
CMD ["node", "src/index.js"]
```

---

## Strategy 4: Security Best Practices

### Use Specific Image Tags

```dockerfile
# ❌ BAD: "latest" can change without warning
FROM node:latest

# ✅ GOOD: Pinned, predictable version
FROM node:18-alpine
```

### Run as Non-Root User

```dockerfile
FROM node:18-alpine
WORKDIR /app

COPY package.json .
RUN npm install --production
COPY . .

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000
CMD ["node", "src/index.js"]
```

### Why Non-Root Matters

```
ROOT user (default):              NON-ROOT user:
┌──────────────────┐             ┌──────────────────┐
│ Container process│             │ Container process│
│ runs as root     │             │ runs as appuser  │
│                  │             │                  │
│ If compromised:  │             │ If compromised:  │
│ Full access to   │             │ Limited access   │
│ container FS     │             │ Can't modify     │
│                  │             │ system files     │
└──────────────────┘             └──────────────────┘
```

---

## Summary: All Best Practices

| Practice | Benefit |
|----------|---------|
| Multi-stage builds | Smaller images, no build tools in production |
| `.dockerignore` | Faster builds, no unnecessary files |
| Layer caching | Faster rebuilds |
| Specific base image tags | Reproducible builds |
| Non-root user | Better security |
| `--production` flag | No devDependencies |
| Alpine-based images | Smaller base (5MB vs 900MB) |

### Size Comparison

```
Base Image Sizes:
┌────────────────────────────────────────────┐
│  node:latest         ████████████  ~900MB  │
│  node:slim           ██████        ~200MB  │
│  node:18-alpine      █             ~50MB   │
└────────────────────────────────────────────┘

Your App:
┌────────────────────────────────────────────┐
│  Single-stage        ██████        ~180MB  │
│  Multi-stage         ████          ~120MB  │
│  + .dockerignore     ███           ~115MB  │
│  + non-root user     ███           ~115MB  │
└────────────────────────────────────────────┘
```

---

## Progressive Hints

<details>
<summary>💡 Hint 1 — Multi-stage structure</summary>

A multi-stage Dockerfile has multiple `FROM` instructions. Each creates a new stage:

```dockerfile
FROM node:18-alpine AS build
# ... build steps ...

FROM node:18-alpine
# ... production steps ...
# COPY --from=build to get artifacts from stage 1
```

</details>

<details>
<summary>💡 Hint 2 — .dockerignore format</summary>

Create `app/.dockerignore` with one pattern per line:

```
node_modules
.git
*.md
```

It works exactly like `.gitignore`.

</details>

<details>
<summary>💡 Hint 3 — Complete multi-stage Dockerfile</summary>

```dockerfile
# Stage 1: Install all deps
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json .
RUN npm install

# Stage 2: Production
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

## Grading Criteria (5 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Multi-stage Dockerfile exists | 3 | File with multiple FROM statements |
| .dockerignore exists | 2 | File that excludes node_modules at minimum |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You created `app/Dockerfile.multistage` with multiple stages
- [ ] You created `app/.dockerignore` excluding unnecessary files
- [ ] The multi-stage image builds successfully
- [ ] The image is smaller than the single-stage version
- [ ] `python run.py --module 11` scores 5/5

---

**Next up:** [Module 12 — What Next?](../12-what-next/README.md) — Where to go from here.
