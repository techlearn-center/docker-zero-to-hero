# Module 12 — What Next?

> **"You've gone from zero to hero. Now where do you go?"** This module maps out your Docker journey beyond this workshop and prepares you for real-world scenarios and interviews.

---

## What You've Accomplished

Let's recap what you've learned:

```
Your Docker Journey
═══════════════════

✅ Module 00 — Installed Docker
✅ Module 01 — Understood what Docker is (and isn't)
✅ Module 02 — Met the todo app
✅ Module 03 — Mastered core concepts (images, containers, registries)
✅ Module 04 — Wrote a Dockerfile and containerized the app
✅ Module 05 — Updated the app and learned about ephemerality
✅ Module 06 — Tagged and shared the image on Docker Hub
✅ Module 07 — Persisted data with volumes
✅ Module 08 — Used bind mounts for development
✅ Module 09 — Connected multiple containers with networks
✅ Module 10 — Simplified everything with Docker Compose
✅ Module 11 — Optimized with multi-stage builds and best practices
```

---

## Skills Checklist

Rate yourself on each skill:

| Skill | Beginner | Intermediate | Confident |
|-------|----------|-------------|-----------|
| Write a Dockerfile | ☐ | ☐ | ☐ |
| Build and tag images | ☐ | ☐ | ☐ |
| Run containers with ports | ☐ | ☐ | ☐ |
| Use volumes for persistence | ☐ | ☐ | ☐ |
| Use bind mounts for development | ☐ | ☐ | ☐ |
| Connect containers with networks | ☐ | ☐ | ☐ |
| Write docker-compose.yml | ☐ | ☐ | ☐ |
| Optimize images (multi-stage) | ☐ | ☐ | ☐ |
| Push/pull from Docker Hub | ☐ | ☐ | ☐ |
| Debug containers (logs, exec) | ☐ | ☐ | ☐ |

---

## Recommended Next Steps

### Level 1: Solidify the Basics

- [ ] Containerize a different app (Python Flask, Go, Java Spring)
- [ ] Try building from a `debian` or `ubuntu` base (not just Alpine)
- [ ] Explore Docker Hub for official images and their Dockerfiles
- [ ] Practice the `docker exec` command for debugging

### Level 2: Expand Your Skills

- [ ] Learn Docker health checks (`HEALTHCHECK` instruction)
- [ ] Explore Docker secrets and configs
- [ ] Set up a CI/CD pipeline that builds Docker images
- [ ] Try Docker Buildx for multi-platform builds (ARM + x86)

### Level 3: Production Ready

- [ ] Learn Kubernetes (container orchestration at scale)
- [ ] Explore container security scanning (Trivy, Snyk)
- [ ] Set up a private registry (Harbor, AWS ECR)
- [ ] Implement logging and monitoring for containers

---

## Interview Preparation

Docker questions come up frequently in DevOps, SRE, and backend interviews. Here are common topics:

### Conceptual Questions

<details>
<summary><strong>Q: What is the difference between an image and a container?</strong></summary>

An **image** is a read-only template containing the application, its dependencies, and instructions for creating a container. A **container** is a running (or stopped) instance of an image. One image can spawn many containers. Think: class vs object in OOP.

</details>

<details>
<summary><strong>Q: How are containers different from VMs?</strong></summary>

Containers share the host OS kernel and isolate at the process level — they're lightweight (MBs) and start in seconds. VMs include a full guest OS and run on a hypervisor — they're heavier (GBs) and start in minutes. Containers provide process isolation; VMs provide full hardware-level isolation.

</details>

<details>
<summary><strong>Q: What is a Docker layer? Why does layer caching matter?</strong></summary>

Each instruction in a Dockerfile creates a layer. Layers are stacked and cached — unchanged layers are reused from cache, making subsequent builds much faster. This is why we copy `package.json` before the source code: if only source code changes, the `npm install` layer stays cached.

</details>

<details>
<summary><strong>Q: What is a multi-stage build?</strong></summary>

A multi-stage build uses multiple `FROM` statements in a single Dockerfile. Each stage can use a different base image. You copy only the needed artifacts from earlier stages to the final image. This produces smaller, more secure production images by excluding build tools and dev dependencies.

</details>

<details>
<summary><strong>Q: Explain volumes vs bind mounts.</strong></summary>

**Volumes** are managed by Docker, stored in Docker's storage area, and ideal for persistent data (databases). **Bind mounts** map a specific host directory into the container, ideal for development (live code editing). Volumes are portable and work the same on all platforms; bind mounts depend on the host filesystem structure.

</details>

### Practical Questions

<details>
<summary><strong>Q: How would you debug a container that keeps crashing?</strong></summary>

1. Check logs: `docker logs <container>`
2. Check the exit code: `docker inspect <container> --format='{{.State.ExitCode}}'`
3. Run interactively: `docker run -it <image> sh` (override CMD)
4. Check resource usage: `docker stats`
5. Inspect the container: `docker inspect <container>`

</details>

<details>
<summary><strong>Q: How do containers communicate with each other?</strong></summary>

Containers on the same Docker network can communicate using container names as hostnames (Docker's built-in DNS). You create a network with `docker network create`, then connect containers with `--network`. Docker Compose creates a network automatically for all services.

</details>

<details>
<summary><strong>Q: How would you reduce a Docker image from 1GB to under 100MB?</strong></summary>

1. Use a smaller base image (Alpine instead of Ubuntu/Debian)
2. Use multi-stage builds to exclude build tools
3. Install only production dependencies (`--production`)
4. Use `.dockerignore` to exclude unnecessary files
5. Combine RUN commands to reduce layers
6. Clean up caches in the same RUN command

</details>

---

## TechLearn Center — Next Challenges

Ready for more? Check out these related challenges:

| Challenge | What You'll Learn |
|-----------|------------------|
| **Kubernetes Basics** | Orchestrate containers at scale |
| **CI/CD Pipeline** | Automate Docker builds in GitHub Actions |
| **Monitoring Stack** | Monitor containers with Prometheus + Grafana |
| **Container Security** | Scan images and secure your containers |
| **Helm Charts** | Package Kubernetes applications |

Visit [github.com/techlearn-center](https://github.com/techlearn-center) to explore all challenges.

---

**Next:** [Module 13 — Educational Resources](../13-educational-resources/README.md) — Curated links, books, and communities.
