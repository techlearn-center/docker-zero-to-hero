# Module 01 — What is Docker?

> **"Imagine packing your entire desk — laptop, files, coffee mug — into a lunchbox that works exactly the same wherever you open it."** That's Docker in a nutshell.

---

## The Problem Docker Solves

You've probably heard (or said) this:

```
"But it works on my machine!" 🤷
```

Here's why that happens:

```
Developer's Laptop          Production Server
┌──────────────────┐       ┌──────────────────┐
│ Node.js 18.17    │       │ Node.js 16.3     │  ← Different version
│ Ubuntu 22.04     │       │ Amazon Linux 2   │  ← Different OS
│ libssl 3.0       │       │ libssl 1.1       │  ← Different library
│ PORT=3000        │       │ PORT=8080        │  ← Different config
└──────────────────┘       └──────────────────┘
         ✅ Works                   ❌ Breaks
```

**Docker's answer:** Package your app *with* its entire environment — OS, libraries, configs, everything — into a single portable unit called a **container**.

---

## The Lunchbox Analogy

Think of it this way:

| Real World | Docker World |
|------------|-------------|
| Recipe (instructions to make food) | **Dockerfile** (instructions to build an image) |
| Packed lunchbox (ready to eat) | **Image** (ready-to-run package) |
| Opening & eating the lunch | **Container** (running instance of an image) |
| Cafeteria / fridge storing lunchboxes | **Registry** (Docker Hub, storing images) |

```
  📝 Recipe          📦 Lunchbox         🍱 Eating
  (Dockerfile)  →    (Image)       →    (Container)
  "How to build"     "Ready to ship"    "Actually running"
```

Key insight: **You write the recipe once. You can pack many identical lunchboxes. Each person opens their own.**

---

## Containers vs Virtual Machines

You might be thinking: "Isn't this just a VM?" Not quite:

```
        Virtual Machines                    Containers
  ┌─────────┐ ┌─────────┐          ┌─────────┐ ┌─────────┐
  │  App A   │ │  App B   │          │  App A   │ │  App B   │
  ├─────────┤ ├─────────┤          ├─────────┤ ├─────────┤
  │ Bins/Lib │ │ Bins/Lib │          │ Bins/Lib │ │ Bins/Lib │
  ├─────────┤ ├─────────┤          └────┬─────┘ └────┬─────┘
  │ Guest OS │ │ Guest OS │               │            │
  ├─────────┤ ├─────────┤          ┌─────┴────────────┴─────┐
  │    Hypervisor         │          │     Container Engine    │
  ├───────────────────────┤          ├────────────────────────┤
  │      Host OS          │          │       Host OS          │
  ├───────────────────────┤          ├────────────────────────┤
  │     Hardware          │          │      Hardware          │
  └───────────────────────┘          └────────────────────────┘

  Each VM = full OS copy              Containers share the host OS
  Heavy (GBs), slow to start          Light (MBs), starts in seconds
```

| Feature | VM | Container |
|---------|-----|-----------|
| Boot time | Minutes | Seconds |
| Size | GBs | MBs |
| Performance | Near-native with overhead | Near-native |
| Isolation | Full OS isolation | Process-level isolation |
| OS | Each VM has its own OS | Shares host kernel |
| Use case | Different OS requirements | Same OS, different apps |

---

## Key Vocabulary

Before we dive deeper, let's define the terms you'll see everywhere:

| Term | Definition |
|------|-----------|
| **Image** | A read-only template containing your app, its dependencies, and instructions for creating a container. Think: blueprint. |
| **Container** | A running instance of an image. Think: a house built from the blueprint. |
| **Dockerfile** | A text file with instructions to build an image. Think: the recipe. |
| **Docker Hub** | A public registry where images are stored and shared. Think: an app store for containers. |
| **Registry** | A service that stores Docker images (Docker Hub is the default public one). |
| **Docker Engine** | The runtime that builds and runs containers. |
| **Docker Desktop** | A GUI application that includes Docker Engine, CLI, and other tools. |

---

## Why Developers Love Docker

1. **Consistency** — Same environment everywhere (dev, staging, prod)
2. **Isolation** — Each app runs in its own container, no conflicts
3. **Speed** — Containers start in seconds, not minutes
4. **Portability** — Build once, run anywhere (laptop, cloud, CI/CD)
5. **Efficiency** — Containers share the host OS, using fewer resources than VMs

---

## Real-World Use Cases

```
┌─────────────────────────────────────────────────────────────┐
│                     Where Docker Shines                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔧 Development    → Consistent dev environments           │
│  🧪 Testing        → Identical test environments           │
│  🚀 CI/CD          → Reproducible build pipelines          │
│  ☁️  Cloud          → Kubernetes orchestration              │
│  🏗️  Microservices  → One container per service             │
│  📦 Distribution   → Ship your app as an image             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Checkpoint ✅

Can you answer these questions?

- [ ] What problem does Docker solve?
- [ ] What's the difference between an image and a container?
- [ ] How are containers different from virtual machines?
- [ ] What is a Dockerfile?

<details>
<summary>💡 Quick self-check answers</summary>

1. Docker solves the "works on my machine" problem by packaging apps with their entire environment.
2. An **image** is a read-only template (blueprint); a **container** is a running instance of that image (the actual house).
3. VMs include a full guest OS (heavy, slow); containers share the host OS kernel (lightweight, fast).
4. A Dockerfile is a text file with instructions to build a Docker image — like a recipe.

</details>

---

**Next up:** [Module 02 — Introduction](../02-introduction/README.md) — Meet the app we'll containerize!
