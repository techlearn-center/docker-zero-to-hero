# Docker Zero to Hero: The Complete Workshop

> **What you'll build:** A containerized todo application from scratch — Dockerfile, multi-container networking, volumes, Docker Compose, and production best practices. By the end, you'll speak Docker fluently.

---

## Quick Start

```bash
# 1. Fork this repository (click "Fork" on GitHub)

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/docker-zero-to-hero.git
cd docker-zero-to-hero

# 3. Start with Module 00 and work through each module in order

# 4. Check your progress at any time
python run.py
```

---

## Workshop Roadmap

```
  FOUNDATIONS                          THE DOCKER WORKSHOP
  ──────────                          ──────────────────
  ┌──────────┐                        ┌───────────────────────────────────────────┐
  │ 00: Get  │                        │                                           │
  │  Docker  │                        │  04: Containerize ──▶ 05: Update          │
  └────┬─────┘                        │       (25 pts)           (10 pts)         │
       │                              │          │                   │            │
  ┌────▼─────┐                        │          ▼                   ▼            │
  │ 01: What │                        │  06: Share ──▶ 07: Persist ──▶ 08: Bind  │
  │is Docker?│                        │   (10 pts)      (10 pts)       (10 pts)  │
  └────┬─────┘                        │                                  │        │
       │                              │                                  ▼        │
  ┌────▼─────┐                        │              09: Multi-Container          │
  │ 02: Intro│                        │                  (15 pts)                 │
  └────┬─────┘                        │                      │                   │
       │                              │                      ▼                   │
  ┌────▼─────┐                        │              10: Docker Compose           │
  │03:Concept│                        │                  (15 pts)                 │
  └────┬─────┘                        │                      │                   │
       │                              │                      ▼                   │
       └──────────────────────────────│              11: Best Practices           │
                                      │                  (5 pts)                  │
                                      └───────────────────────────────────────────┘
                                                             │
  WRAP-UP                                                    │
  ───────                                                    │
  ┌──────────┐   ┌──────────┐                                │
  │ 12: What │◀──┤13:Resourc│◀───────────────────────────────┘
  │   Next   │   │    es    │
  └──────────┘   └──────────┘
```

---

## Module Navigation

| # | Module | Type | Points | What You'll Do |
|---|--------|------|--------|----------------|
| 00 | [Get Docker](./00-get-docker/) | Setup | -- | Install Docker and verify it works |
| 01 | [What is Docker?](./01-what-is-docker/) | Conceptual | -- | Understand containers, VMs, and why Docker exists |
| 02 | [Introduction](./02-introduction/) | Conceptual | -- | Meet the app and learn the workshop structure |
| 03 | [Docker Concepts](./03-docker-concepts/) | Conceptual | -- | Images, layers, containers, registries, networking |
| 04 | [Containerize an Application](./04-containerize-application/) | Hands-on | 25 | Write a Dockerfile and build your first image |
| 05 | [Update the Application](./05-update-application/) | Hands-on | 10 | Edit code, rebuild, learn the update workflow |
| 06 | [Share the Application](./06-share-application/) | Hands-on | 10 | Tag and push your image to Docker Hub |
| 07 | [Persist the DB](./07-persist-the-db/) | Hands-on | 10 | Use volumes to keep data across restarts |
| 08 | [Use Bind Mounts](./08-use-bind-mounts/) | Hands-on | 10 | Live development workflow with code syncing |
| 09 | [Multi-Container Apps](./09-multi-container-apps/) | Hands-on | 15 | Add MySQL in a separate container with networking |
| 10 | [Use Docker Compose](./10-use-docker-compose/) | Hands-on | 15 | Define your stack in YAML, run with one command |
| 11 | [Image-Building Best Practices](./11-image-building-best-practices/) | Hands-on | 5 | Multi-stage builds, .dockerignore, optimization |
| 12 | [What Next](./12-what-next/) | Reference | -- | Interview prep, next challenges, advanced topics |
| 13 | [Educational Resources](./13-educational-resources/) | Reference | -- | Books, videos, communities, cheat sheets |

---

## Points and Grading

| Requirement | Value |
|------------|-------|
| **Total points** | 100 |
| **Passing score** | 70 |
| **Graded modules** | 04 through 11 |

### Check Your Progress

```bash
python run.py
```

The grading script validates your Dockerfile, docker-compose.yml, and other artifacts automatically.

### Points Breakdown

| Module | Points | What's Graded |
|--------|--------|---------------|
| 04 - Containerize | 25 | Dockerfile structure, builds, runs |
| 05 - Update | 10 | Source code modified, image rebuilds |
| 06 - Share | 10 | Image tagging format |
| 07 - Persist | 10 | Volume configuration |
| 08 - Bind Mounts | 10 | Bind mount workflow |
| 09 - Multi-Container | 15 | Network + MySQL configuration |
| 10 - Docker Compose | 15 | docker-compose.yml with both services |
| 11 - Best Practices | 5 | Multi-stage build, .dockerignore |

---

## The Application

You'll work with a **Todo App** — a web application for managing a task list.

```
┌────────────────────────────────────┐
│  Todo App                          │
│  Docker Zero-to-Hero Workshop      │
│                                    │
│  ┌──────────────────────┐ ┌─────┐ │
│  │ What needs to be done│ │ Add │ │
│  └──────────────────────┘ └─────┘ │
│                                    │
│  ☑ Learn Docker basics             │
│  ☐ Write a Dockerfile              │
│  ☐ Use Docker Compose              │
│                                    │
└────────────────────────────────────┘
```

**Tech stack:** Node.js + Express, SQLite (local) / MySQL (multi-container)

---

## Prerequisites

- A computer with admin/root access
- Basic command line knowledge (terminal/PowerShell)
- A text editor (VS Code recommended)
- A web browser

**You do NOT need:**
- Prior Docker experience
- Deep programming knowledge
- A cloud account

---

## Repository Structure

```
docker-zero-to-hero/
├── README.md                    ← You are here
├── challenge.json               # Workshop metadata
├── run.py                       # Automated grading script
├── docker-compose.yml           # Starter file for Module 10
├── app/                         # The todo application
│   ├── Dockerfile               # Starter file for Module 04
│   ├── package.json
│   └── src/                     # Application source code
├── 00-get-docker/               # Module READMEs
├── 01-what-is-docker/
├── ...
├── 13-educational-resources/
└── resources/
    └── cheatsheets/
        └── docker-commands.md   # Command reference
```

---

## License

This workshop is open source and available for educational purposes.

---

**Built with care by [TechLearn Center](https://github.com/techlearn-center)**
