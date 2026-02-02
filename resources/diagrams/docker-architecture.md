# Docker Architecture Diagrams

Visual references for understanding how Docker components work together.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Docker Client                         │
│                  (docker CLI / Docker Desktop)                │
│                                                             │
│   docker build    docker run    docker pull    docker push   │
└──────────┬──────────┬──────────────┬──────────────┬─────────┘
           │          │              │              │
           │     REST API            │              │
           │          │              │              │
┌──────────▼──────────▼──────────────▼──────────────▼─────────┐
│                      Docker Daemon (dockerd)                 │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │   Images     │  │  Containers  │  │    Networks         │ │
│  │             │  │              │  │                    │ │
│  │ ┌─────────┐ │  │ ┌──────────┐│  │ bridge  host  none │ │
│  │ │ node:18 │ │  │ │ todo-app ││  │                    │ │
│  │ │ mysql:8 │ │  │ │ mysql    ││  │ custom networks    │ │
│  │ │ todo-app│ │  │ └──────────┘│  └────────────────────┘ │
│  │ └─────────┘ │  └──────────────┘                        │
│  └─────────────┘                    ┌────────────────────┐ │
│                                     │    Volumes          │ │
│                                     │                    │ │
│                                     │ todo-db            │ │
│                                     │ mysql-data         │ │
│                                     └────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
           │                                      │
           │  pull / push                         │
           ▼                                      │
┌─────────────────────┐                           │
│    Registry          │                           │
│  (Docker Hub)        │                           │
│                     │                  Host Filesystem
│  node:18-alpine     │                           │
│  mysql:8.0          │                           │
│  user/todo-app:1.0  │                           │
└─────────────────────┘                           │
```

---

## Image Build Process

```
  Dockerfile                    Build Process                  Image
  ┌──────────────┐             ┌──────────────┐             ┌──────────────┐
  │ FROM node:18 │──Step 1───→ │ Pull base    │──Layer 1──→ │ ████████████ │
  │              │             │ image        │             │              │
  │ WORKDIR /app │──Step 2───→ │ Set working  │──Layer 2──→ │ ████████████ │
  │              │             │ directory    │             │ ████████     │
  │ COPY pkg.json│──Step 3───→ │ Copy file    │──Layer 3──→ │ ████████████ │
  │              │             │              │             │ ████████     │
  │ RUN npm i    │──Step 4───→ │ Install deps │──Layer 4──→ │ ██████       │
  │              │             │              │             │ ████████████ │
  │ COPY . .     │──Step 5───→ │ Copy source  │──Layer 5──→ │ ████████████ │
  │              │             │              │             │ ████████     │
  │ EXPOSE 3000  │──Step 6───→ │ Metadata     │             │ ██████       │
  │              │             │              │──Layer 6──→ │ ████████████ │
  │ CMD [...]    │──Step 7───→ │ Metadata     │             │ ████████████ │
  └──────────────┘             └──────────────┘             └──────────────┘
                                                               todo-app
                                                               ~180 MB
```

---

## Container Lifecycle

```
                 docker create
                      │
                      ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │          │   │          │   │          │   │          │
  │  Image   │──→│ Created  │──→│ Running  │──→│ Stopped  │──→ Removed
  │          │   │          │   │          │   │          │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘
                  docker run     docker stop     docker rm
                  docker start   Ctrl+C
                                 app exits

                                 docker restart
                                 ┌──────────┐
                                 │          │
                           ┌─────│ Running  │─────┐
                           │     │          │     │
                           │     └──────────┘     │
                           │     docker restart   │
                           └──────────────────────┘
```

---

## Networking Model

```
  Host Machine (your laptop)
  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │   Browser → localhost:3000                       │
  │                  │                               │
  │            port mapping                          │
  │             -p 3000:3000                          │
  │                  │                               │
  │   ┌── Docker Network (bridge) ──────────────┐    │
  │   │              │                          │    │
  │   │   ┌──────────▼──────┐  ┌─────────────┐ │    │
  │   │   │    todo-app     │  │    mysql     │ │    │
  │   │   │   (web server)  │  │  (database)  │ │    │
  │   │   │                 │  │              │ │    │
  │   │   │  172.18.0.2     │  │ 172.18.0.3  │ │    │
  │   │   │  :3000          │  │ :3306       │ │    │
  │   │   └────────┬────────┘  └──────▲──────┘ │    │
  │   │            │                  │        │    │
  │   │            └──DNS: "mysql"────┘        │    │
  │   │                                        │    │
  │   └────────────────────────────────────────┘    │
  │                                                  │
  └──────────────────────────────────────────────────┘
```

---

## Volume Types

```
  ┌─────────────────────────────────────────────────────────┐
  │                      Container                          │
  │                                                         │
  │   /app/data ──────┐   /app/src ──────┐   /tmp ────┐    │
  │                   │                  │            │    │
  └───────────────────┼──────────────────┼────────────┼────┘
                      │                  │            │
              ┌───────▼──────┐  ┌────────▼───────┐  ┌▼────────┐
              │ Named Volume │  │  Bind Mount    │  │  tmpfs   │
              │              │  │                │  │          │
              │ Managed by   │  │ Maps to a      │  │ RAM only │
              │ Docker       │  │ specific host  │  │ Never    │
              │              │  │ directory      │  │ written  │
              │ /var/lib/    │  │                │  │ to disk  │
              │ docker/      │  │ $(pwd)/app/src │  │          │
              │ volumes/     │  │                │  │          │
              │ todo-db/     │  │ You control    │  │ Fast,    │
              │              │  │ the path       │  │ secure   │
              │ Best for:    │  │                │  │          │
              │ databases    │  │ Best for:      │  │ Best for:│
              │ uploads      │  │ development    │  │ secrets  │
              │ persistent   │  │ config files   │  │ temp     │
              │ data         │  │                │  │ data     │
              └──────────────┘  └────────────────┘  └──────────┘
```

---

## Docker Compose Multi-Container

```
  docker-compose.yml
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  services:                                              │
  │                                                         │
  │    ┌───────────────┐          ┌───────────────┐         │
  │    │     web        │         │    mysql       │         │
  │    │               │         │               │         │
  │    │ build: ./app  │ ──────→ │ image: mysql:8│         │
  │    │ ports: 3000   │ network │ env: ROOT_PASS│         │
  │    │ env: MYSQL_*  │         │               │         │
  │    │ depends_on:   │         │               │         │
  │    │   - mysql     │         │               │         │
  │    └───────────────┘         └───────┬───────┘         │
  │                                      │                 │
  │  volumes:                            │                 │
  │    ┌─────────────┐                   │                 │
  │    │ mysql-data   │ ←────────────────┘                 │
  │    │ /var/lib/    │  /var/lib/mysql                    │
  │    │ mysql        │                                    │
  │    └─────────────┘                                     │
  │                                                         │
  │  networks: (auto-created)                               │
  │    ┌─────────────────────────────────────────────┐     │
  │    │ project_default                              │     │
  │    │   web ←──DNS──→ mysql                       │     │
  │    └─────────────────────────────────────────────┘     │
  │                                                         │
  └─────────────────────────────────────────────────────────┘

  One command: docker compose up -d
  Creates: network + volumes + containers
  Destroys: docker compose down
```

---

## Multi-Stage Build

```
  Dockerfile (multi-stage)

  Stage 1: "deps"                    Stage 2: "production"
  ┌────────────────────┐            ┌────────────────────┐
  │ FROM node:18-alpine│            │ FROM node:18-alpine│
  │ AS deps            │            │                    │
  │                    │            │ COPY package.json  │
  │ COPY package.json  │            │ RUN npm install    │
  │ RUN npm install    │  ──copy──→ │   --production     │
  │  (all deps)        │  artifacts │ COPY . .           │
  │                    │            │                    │
  │ Size: ~200MB       │            │ Size: ~120MB       │
  │ Contains:          │            │ Contains:          │
  │  - dev deps        │  DISCARD   │  - prod deps only  │
  │  - test tools      │ ←─────────│  - app source      │
  │  - build tools     │            │  - no dev tools    │
  └────────────────────┘            └────────────────────┘
   Thrown away after build           This becomes your image
```

---

**[Back to Workshop Home](../../README.md)**
