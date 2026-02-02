# Module 03 — Docker Concepts

> **"Before you build a house, understand the blueprint."** This module covers the core concepts you'll use in every Docker workflow: images, containers, layers, registries, and the build context.

---

## The Docker Workflow

Every Docker workflow follows this pattern:

```
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │          │      │          │      │          │
  │Dockerfile│─────→│  Image   │─────→│Container │
  │          │build │          │ run  │          │
  │ (recipe) │      │(package) │      │(running) │
  └──────────┘      └──────────┘      └──────────┘
       │                 │                  │
    You write        Docker builds      Docker runs
    instructions     a snapshot         a process
```

---

## Images

An image is a **read-only template** that contains:
- A base operating system (e.g., Alpine Linux)
- Your application code
- Dependencies (e.g., Node.js, Python packages)
- Configuration and environment variables
- Instructions for how to start your app

### Images Are Made of Layers

Each instruction in a Dockerfile creates a **layer**. Layers are stacked and cached:

```
┌───────────────────────────┐
│  CMD ["node", "index.js"] │  Layer 5 (metadata)
├───────────────────────────┤
│  COPY . .                 │  Layer 4 (your code)
├───────────────────────────┤
│  RUN npm install          │  Layer 3 (dependencies)
├───────────────────────────┤
│  COPY package.json .      │  Layer 2 (package.json)
├───────────────────────────┤
│  FROM node:18-alpine      │  Layer 1 (base image)
└───────────────────────────┘
```

**Why layers matter:**
- Layers are **cached** — if a layer hasn't changed, Docker reuses it
- Only **changed layers** (and layers above them) are rebuilt
- This makes builds **fast** after the first time

### Layer Caching in Action

```
First build:                    Second build (only code changed):

Layer 5: CMD           NEW      Layer 5: CMD           CACHED → rebuilt
Layer 4: COPY . .      NEW      Layer 4: COPY . .      CHANGED → rebuilt
Layer 3: npm install   NEW      Layer 3: npm install   CACHED ✓
Layer 2: COPY pkg.json NEW      Layer 2: COPY pkg.json CACHED ✓
Layer 1: FROM node     NEW      Layer 1: FROM node     CACHED ✓

Total: ~60 seconds              Total: ~3 seconds
```

This is why we copy `package.json` **before** the rest of the code — the dependency install layer stays cached unless `package.json` changes.

---

## Containers

A container is a **running instance** of an image. Think of the relationship like this:

```
  Image (Class)              Container (Object/Instance)
  ┌──────────────┐           ┌──────────────┐
  │              │     ┌────→│ Container A   │  (running)
  │  node:18     │     │     └──────────────┘
  │  + your app  │─────┤
  │  + deps      │     │     ┌──────────────┐
  │              │     └────→│ Container B   │  (running)
  └──────────────┘           └──────────────┘

  One image → many containers (each isolated)
```

### Container Properties

| Property | Description |
|----------|-------------|
| **Isolated** | Each container has its own filesystem, network, and process space |
| **Ephemeral** | When a container is removed, its data is lost (unless you use volumes) |
| **Lightweight** | Containers share the host OS kernel — no full OS per container |
| **Portable** | A container runs the same everywhere Docker is installed |

### Container Lifecycle

```
  Created ──→ Running ──→ Stopped ──→ Removed
     │            │            │           │
  docker run  (running)   docker stop  docker rm
  docker create            Ctrl+C
```

---

## Registries

A registry is a **storage and distribution system** for Docker images:

```
┌──────────────┐    docker push    ┌──────────────────┐
│  Your Machine │ ───────────────→ │   Docker Hub     │
│              │                   │  (Registry)      │
│  myapp:1.0   │ ←─────────────── │                  │
│              │    docker pull    │  myapp:1.0       │
└──────────────┘                   └──────────────────┘
                                          │
                                    docker pull
                                          │
                                   ┌──────────────┐
                                   │  Server /    │
                                   │  Colleague   │
                                   │  myapp:1.0   │
                                   └──────────────┘
```

### Common Registries

| Registry | URL | Use Case |
|----------|-----|----------|
| Docker Hub | hub.docker.com | Default public registry |
| GitHub Container Registry | ghcr.io | GitHub-integrated |
| Amazon ECR | aws.amazon.com/ecr | AWS workloads |
| Google Artifact Registry | cloud.google.com/artifact-registry | GCP workloads |
| Azure Container Registry | azure.microsoft.com/services/container-registry | Azure workloads |

### Image Naming Convention

```
  registry/username/repository:tag

  Examples:
  ─────────────────────────────────────────────────────
  docker.io/library/node:18-alpine    (official image)
  docker.io/myuser/myapp:1.0          (user image)
  ghcr.io/myorg/myapp:latest          (GitHub registry)

  Short form (Docker Hub assumed):
  node:18-alpine
  myuser/myapp:1.0
```

---

## The Build Context

When you run `docker build`, Docker sends a **build context** to the Docker daemon:

```bash
docker build -t myapp .
                      ^
                      └── This dot = build context (current directory)
```

```
┌────────────────────────────────────────┐
│  Build Context = everything in "."     │
│                                        │
│  ├── package.json       ✅ Sent        │
│  ├── src/               ✅ Sent        │
│  ├── node_modules/      ❌ Wasteful!   │
│  ├── .git/              ❌ Wasteful!   │
│  └── .env               ❌ Dangerous!  │
│                                        │
│  Solution: Use a .dockerignore file    │
└────────────────────────────────────────┘
```

### .dockerignore

Works like `.gitignore` — tells Docker what to exclude from the build context:

```
node_modules
.git
.env
*.md
.DS_Store
```

This makes builds **faster** (less data to send) and **safer** (no secrets in the image).

---

## Putting It All Together

Here's the complete picture of how Docker components interact:

```
 Developer                Docker Engine               Registry
 ┌────────┐              ┌──────────────┐           ┌──────────┐
 │        │  Dockerfile  │              │  push     │          │
 │  You   │────────────→ │   Build      │─────────→ │  Docker  │
 │        │              │   Image      │           │  Hub     │
 │        │              │              │  pull     │          │
 │        │              │   Run        │←───────── │          │
 │        │  docker run  │   Container  │           │          │
 │        │────────────→ │              │           │          │
 └────────┘              └──────────────┘           └──────────┘
```

---

## Key Commands Preview

You'll learn these commands in detail in the hands-on modules:

| Command | What It Does |
|---------|-------------|
| `docker build -t name .` | Build an image from a Dockerfile |
| `docker run name` | Create and start a container from an image |
| `docker ps` | List running containers |
| `docker stop <id>` | Stop a running container |
| `docker rm <id>` | Remove a stopped container |
| `docker images` | List local images |
| `docker push name` | Push an image to a registry |
| `docker pull name` | Pull an image from a registry |

---

## Checkpoint ✅

Can you answer these questions?

- [ ] What is a Docker image layer? Why do layers matter?
- [ ] What happens to data inside a container when it's removed?
- [ ] What is the build context? Why should you use `.dockerignore`?
- [ ] What is a registry? Name two examples.

<details>
<summary>💡 Quick self-check answers</summary>

1. A **layer** is created by each Dockerfile instruction. Layers are cached so unchanged layers don't need to be rebuilt — this speeds up builds dramatically.
2. Data is **lost** when a container is removed — containers are ephemeral. To persist data, you need **volumes** (Module 07).
3. The **build context** is the directory sent to Docker when building an image (the `.` in `docker build .`). Use `.dockerignore` to exclude unnecessary/sensitive files, making builds faster and safer.
4. A **registry** stores and distributes Docker images. Examples: Docker Hub, GitHub Container Registry (ghcr.io), Amazon ECR.

</details>

---

**Next up:** [Module 04 — Containerize the Application](../04-containerize-application/README.md) — Time to write your first Dockerfile! 🎯
