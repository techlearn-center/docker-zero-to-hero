# Module 02 — Introduction

> **"The best way to learn Docker is to actually Docker something."** In this module, you'll meet the app we'll containerize throughout this workshop and understand how this learning path is structured.

---

## Workshop Roadmap

Here's the journey from zero to hero:

```
  YOU ARE HERE
      ↓
  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
  │ 00 Setup │────→│ 01 What │────→│ 02 Intro │────→│ 03 Core │
  │          │     │  is it? │     │  (here!) │     │Concepts │
  └─────────┘     └─────────┘     └─────────┘     └────┬────┘
                                                        │
  ┌─────────────────────────────────────────────────────┘
  │
  │  THE WORKSHOP (Hands-On)
  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐
  ├─→│ 04       │──→│ 05       │──→│ 06       │
  │  │Container-│   │ Update   │   │ Share    │
  │  │ize App   │   │ the App  │   │ the App  │
  │  │ (25 pts) │   │ (10 pts) │   │ (10 pts) │
  │  └──────────┘   └──────────┘   └──────────┘
  │
  │  ┌──────────┐   ┌──────────┐
  ├─→│ 07       │──→│ 08       │
  │  │ Persist  │   │ Bind     │
  │  │ the DB   │   │ Mounts   │
  │  │ (10 pts) │   │ (10 pts) │
  │  └──────────┘   └──────────┘
  │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐
  └─→│ 09       │──→│ 10       │──→│ 11 Best  │
     │ Multi-   │   │ Docker   │   │Practices │
     │Container │   │ Compose  │   │ (5 pts)  │
     │ (15 pts) │   │ (15 pts) │   └──────────┘
     └──────────┘   └──────────┘
```

---

## Meet the App: Todo App

Throughout this workshop, you'll work with a **Node.js todo application**. It's intentionally simple so you can focus on Docker concepts rather than app complexity.

### What It Does

```
┌─────────────────────────────────────────┐
│  Todo App - Docker Workshop             │
├─────────────────────────────────────────┤
│                                         │
│  [ What needs to be done?    ] [Add]    │
│                                         │
│  ☑ Learn Docker basics                  │
│  ☐ Write a Dockerfile                   │
│  ☐ Build an image                       │
│  ☐ Run a container                      │
│                                         │
└─────────────────────────────────────────┘
```

- **Add** todos
- **Check off** completed todos
- **Delete** todos
- Data stored in **SQLite** (local) or **MySQL** (multi-container)

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Node.js + Express |
| Database | SQLite (local) / MySQL (multi-container) |
| Frontend | Vanilla HTML/CSS/JS |
| Health check | `/healthz` endpoint |

### Project Structure

```
app/
├── package.json          # Dependencies & scripts
├── Dockerfile            # ← YOU WILL COMPLETE THIS (Module 04)
├── src/
│   ├── index.js          # Express server (port 3000)
│   ├── routes/
│   │   ├── todos.js      # CRUD API routes
│   │   └── health.js     # Health check endpoint
│   ├── persistence/
│   │   ├── sqlite.js     # SQLite adapter
│   │   └── mysql.js      # MySQL adapter
│   └── static/
│       ├── index.html    # Frontend UI
│       ├── css/styles.css
│       └── js/app.js
└── spec/
    └── todos.spec.js     # Basic tests
```

---

## How This Workshop Works

### Learning by Doing

Each hands-on module follows this pattern:

1. **Read** the concept explanation
2. **Do** the hands-on exercise
3. **Check** your work with the checkpoint
4. **Explore** the progressive hints if you get stuck

### Progressive Hints

Stuck? Each module has expandable hints that give you progressively more detail:

<details>
<summary>💡 Hint 1 — Nudge in the right direction</summary>

This is a gentle hint that points you the right way without giving the answer.

</details>

<details>
<summary>💡 Hint 2 — More specific guidance</summary>

This narrows it down further with more specific instructions.

</details>

<details>
<summary>💡 Hint 3 — Almost the answer</summary>

This is basically the answer with just a small gap for you to fill.

</details>

### Point System

The hands-on modules (04–11) are graded automatically:

| Score | Status |
|-------|--------|
| 70–100 | ✅ **Passing** — You've mastered the Docker basics! |
| 50–69 | 🔶 **Getting there** — Review the modules you missed |
| 0–49 | 🔴 **Keep going** — Focus on modules 04, 09, and 10 first |

Run the grader anytime:

```bash
python run.py
```

Or check a specific module:

```bash
python run.py --module 04
```

---

## Prerequisites

Before starting the hands-on modules, make sure you have:

- [ ] Docker installed and running ([Module 00](../00-get-docker/README.md))
- [ ] A text editor (VS Code recommended)
- [ ] A terminal / command prompt
- [ ] Basic command-line knowledge (`cd`, `ls`, `mkdir`)
- [ ] (Optional) A Docker Hub account for Module 06

You do **not** need to know Node.js — the app code is provided and explained where relevant.

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You understand the workshop structure (conceptual → hands-on → reference)
- [ ] You've looked at the `app/` directory structure
- [ ] You know how to run the grader (`python run.py`)
- [ ] Docker is installed and running

---

**Next up:** [Module 03 — Docker Concepts](../03-docker-concepts/README.md) — Understand images, containers, and registries before we build.
