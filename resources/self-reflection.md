# Self-Reflection & Learning Journal

Use this guide after each module to reflect on what you learned, what confused you, and how it connects to real-world work. Writing down your thoughts solidifies understanding and reveals gaps.

---

## How to Use This Guide

After completing each module:
1. Answer the reflection questions honestly (no one is grading this)
2. Rate your confidence level
3. Write down one thing you'd explain to a colleague
4. Note any questions that remain unanswered

---

## Module 00 — Get Docker

### Reflection Questions

- What operating system are you using? Did you encounter any installation issues?
- Did the `docker run hello-world` output make sense to you, or was it confusing?
- Before this module, had you used any containerization or virtualization tools?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Installing Docker | ☐ | ☐ | ☐ |
| Verifying Docker works | ☐ | ☐ | ☐ |
| Running a basic container | ☐ | ☐ | ☐ |

### Teach-Back

> In one sentence, explain to a colleague what Docker is and how they can verify it's installed.

_Your answer:_

---

## Module 01 — What is Docker?

### Reflection Questions

- Before reading this module, what did you think Docker was? How has your understanding changed?
- Can you think of a time at work where Docker would have helped? (e.g., "it works on my machine" situations, environment mismatches)
- Which analogy helped you most — the lunchbox analogy or the class/object analogy?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Explaining Docker's purpose | ☐ | ☐ | ☐ |
| Distinguishing images from containers | ☐ | ☐ | ☐ |
| Explaining containers vs VMs | ☐ | ☐ | ☐ |

### Teach-Back

> Explain to a non-technical person what Docker does and why developers use it.

_Your answer:_

---

## Module 02 — Introduction

### Reflection Questions

- Looking at the todo app's code, what felt familiar? What was new?
- Do you understand why the app can switch between SQLite and MySQL? What triggers the switch?
- How do you feel about the grading system? Does the point breakdown motivate you?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Navigating the project structure | ☐ | ☐ | ☐ |
| Understanding the app's tech stack | ☐ | ☐ | ☐ |
| Running the grading script | ☐ | ☐ | ☐ |

### Teach-Back

> Describe how the todo app works in 2-3 sentences, including what technologies it uses.

_Your answer:_

---

## Module 03 — Docker Concepts

### Reflection Questions

- Which concept was hardest to grasp: layers, registries, or the build context?
- Can you trace the full lifecycle of a container from creation to removal?
- Why is layer caching important? What would happen without it?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Explaining Docker layers and caching | ☐ | ☐ | ☐ |
| Understanding the build context | ☐ | ☐ | ☐ |
| Knowing when to use .dockerignore | ☐ | ☐ | ☐ |
| Understanding registries | ☐ | ☐ | ☐ |

### Teach-Back

> Explain to someone why we copy `package.json` before the rest of the source code in a Dockerfile.

_Your answer:_

---

## Module 04 — Containerize the Application

### Reflection Questions

- Writing the Dockerfile — was it easier or harder than you expected?
- Did you get it right on the first try, or did you need the hints? (No shame either way!)
- When you ran `docker build`, did you notice the layer numbers in the output? Can you map them to your Dockerfile instructions?
- What did it feel like to see the app running at `localhost:3000` inside a container?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Writing a Dockerfile from scratch | ☐ | ☐ | ☐ |
| Building an image with `docker build` | ☐ | ☐ | ☐ |
| Running a container with port mapping | ☐ | ☐ | ☐ |
| Understanding each Dockerfile instruction | ☐ | ☐ | ☐ |

### Teach-Back

> Walk someone through the 7 instructions in your Dockerfile and explain why each one is needed.

_Your answer:_

---

## Module 05 — Update the Application

### Reflection Questions

- Were you surprised by how fast the rebuild was? Why was it fast?
- When you got the "port already allocated" error — did you understand immediately why, or did you need to think about it?
- The key lesson: data is lost when a container is removed. How does this change how you think about containers?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Rebuilding images after code changes | ☐ | ☐ | ☐ |
| Stopping and replacing containers | ☐ | ☐ | ☐ |
| Understanding container ephemerality | ☐ | ☐ | ☐ |

### Teach-Back

> Explain the update workflow (edit → build → stop → run) and why data doesn't persist.

_Your answer:_

---

## Module 06 — Share the Application

### Reflection Questions

- Did you create a Docker Hub account? If you already had one, when did you first create it?
- Does the image naming convention (registry/username/repo:tag) make sense?
- Can you think of scenarios at work where pushing images to a registry would be useful?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Tagging images correctly | ☐ | ☐ | ☐ |
| Pushing to Docker Hub | ☐ | ☐ | ☐ |
| Understanding image naming | ☐ | ☐ | ☐ |

### Teach-Back

> Explain the push/pull workflow: how does an image get from your laptop to a colleague's machine?

_Your answer:_

---

## Module 07 — Persist the DB

### Reflection Questions

- Before this module, how would you have solved the data loss problem? Did volumes match your expectation?
- Can you articulate the difference between data living inside a container vs. data living in a volume?
- What would happen if two containers mounted the same volume?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Creating and using named volumes | ☐ | ☐ | ☐ |
| Understanding mount points | ☐ | ☐ | ☐ |
| Choosing between volume types | ☐ | ☐ | ☐ |

### Teach-Back

> Explain to someone why we need volumes, using the todo app's SQLite database as a concrete example.

_Your answer:_

---

## Module 08 — Use Bind Mounts

### Reflection Questions

- How did it feel to edit a file and see the change instantly without rebuilding?
- Can you explain why the anonymous volume for `node_modules` is necessary?
- When would you use a bind mount vs. a named volume? Give an example of each.

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Using bind mounts for development | ☐ | ☐ | ☐ |
| Understanding the node_modules trick | ☐ | ☐ | ☐ |
| Choosing volumes vs bind mounts | ☐ | ☐ | ☐ |

### Teach-Back

> Explain the development workflow with bind mounts: what happens when you save a file?

_Your answer:_

---

## Module 09 — Multi-Container Apps

### Reflection Questions

- Was connecting two containers harder or easier than expected?
- The fact that container names become DNS hostnames — did that surprise you?
- How does this module change your thinking about application architecture?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Creating Docker networks | ☐ | ☐ | ☐ |
| Running multi-container setups | ☐ | ☐ | ☐ |
| Configuring environment variables | ☐ | ☐ | ☐ |
| Understanding container DNS | ☐ | ☐ | ☐ |

### Teach-Back

> Explain how the todo app connects to MySQL in a multi-container setup — what makes the name "mysql" resolve to the database?

_Your answer:_

---

## Module 10 — Use Docker Compose

### Reflection Questions

- Compare the `docker run` commands from Module 09 to the `docker-compose.yml`. Which is easier to understand?
- If you had to add a Redis cache to this setup, could you do it? What would you add to the YAML?
- How does `docker compose down -v` differ from `docker compose down`? Why is this distinction important?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Writing docker-compose.yml | ☐ | ☐ | ☐ |
| Starting/stopping with Compose | ☐ | ☐ | ☐ |
| Defining services, volumes, networks | ☐ | ☐ | ☐ |
| Understanding depends_on | ☐ | ☐ | ☐ |

### Teach-Back

> Explain Docker Compose to someone who just finished Module 09 — why is Compose better than manual `docker run` commands?

_Your answer:_

---

## Module 11 — Image Building Best Practices

### Reflection Questions

- What was the size difference between your single-stage and multi-stage images?
- Which best practice do you think has the biggest impact: multi-stage builds, .dockerignore, or layer ordering?
- Would you apply these practices to a real project? What would you prioritize first?

### Confidence Check

| Skill | Not Yet | Getting There | Confident |
|-------|---------|---------------|-----------|
| Writing multi-stage Dockerfiles | ☐ | ☐ | ☐ |
| Creating effective .dockerignore | ☐ | ☐ | ☐ |
| Optimizing layer order | ☐ | ☐ | ☐ |
| Running as non-root | ☐ | ☐ | ☐ |

### Teach-Back

> Explain to someone how to reduce a Docker image from 900MB to under 100MB, step by step.

_Your answer:_

---

## Overall Workshop Reflection

### The Big Picture

Answer these after completing all modules:

1. **What was the most valuable thing you learned?**

   _Your answer:_

2. **What concept or module was the hardest? Why?**

   _Your answer:_

3. **How has your understanding of containerization changed from Module 00 to now?**

   _Your answer:_

4. **Name three ways Docker could improve your current work or projects.**

   a. _

   b. _

   c. _

5. **What would you do differently if you went through this workshop again?**

   _Your answer:_

6. **What's the next Docker-related skill you want to learn?**

   _Your answer:_

### Final Confidence Summary

| Skill Area | Before Workshop | After Workshop |
|------------|----------------|----------------|
| Docker fundamentals | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |
| Writing Dockerfiles | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |
| Docker Compose | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |
| Multi-container apps | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |
| Image optimization | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |
| Docker networking | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |
| Docker volumes | ☐ None ☐ Basic ☐ Intermediate | ☐ Basic ☐ Intermediate ☐ Confident |

---

**[Back to Workshop Home](../README.md)**
