# Exercise: Docker Concepts Matching

## Part 1 — Match the Command to Its Purpose

Draw a line (or just note the letter) matching each command to what it does:

| # | Command | | Purpose |
|---|---------|---|---------|
| 1 | `docker build -t myapp .` | | A. Stop a running container |
| 2 | `docker run -dp 3000:3000 myapp` | | B. List running containers |
| 3 | `docker ps` | | C. Push image to a registry |
| 4 | `docker stop abc123` | | D. Build an image from a Dockerfile |
| 5 | `docker push myapp:1.0` | | E. Run a container in background with port mapping |
| 6 | `docker images` | | F. Remove a stopped container |
| 7 | `docker rm abc123` | | G. List local images |

<details>
<summary>Show Answers</summary>

| # | Command | Answer |
|---|---------|--------|
| 1 | `docker build -t myapp .` | **D** — Build an image from a Dockerfile |
| 2 | `docker run -dp 3000:3000 myapp` | **E** — Run a container in background with port mapping |
| 3 | `docker ps` | **B** — List running containers |
| 4 | `docker stop abc123` | **A** — Stop a running container |
| 5 | `docker push myapp:1.0` | **C** — Push image to a registry |
| 6 | `docker images` | **G** — List local images |
| 7 | `docker rm abc123` | **F** — Remove a stopped container |

</details>

---

## Part 2 — Match the Concept to Its Definition

| # | Concept | | Definition |
|---|---------|---|-----------|
| 1 | Image Layer | | A. A service that stores and distributes Docker images |
| 2 | Build Context | | B. A running instance of a Docker image |
| 3 | Registry | | C. The directory sent to Docker daemon during `docker build` |
| 4 | Container | | D. A read-only snapshot created by each Dockerfile instruction |
| 5 | .dockerignore | | E. A file specifying what to exclude from the build context |

<details>
<summary>Show Answers</summary>

| # | Concept | Answer |
|---|---------|--------|
| 1 | Image Layer | **D** — A read-only snapshot created by each Dockerfile instruction |
| 2 | Build Context | **C** — The directory sent to Docker daemon during `docker build` |
| 3 | Registry | **A** — A service that stores and distributes Docker images |
| 4 | Container | **B** — A running instance of a Docker image |
| 5 | .dockerignore | **E** — A file specifying what to exclude from the build context |

</details>

---

## Part 3 — True or False

| # | Statement | Your Answer |
|---|-----------|-------------|
| 1 | Containers share the host operating system's kernel | |
| 2 | Each Docker image contains a full copy of an operating system like a VM | |
| 3 | Docker layers are cached to speed up subsequent builds | |
| 4 | When a container is removed, its data is preserved automatically | |
| 5 | You can run multiple containers from a single image | |
| 6 | The `.` in `docker build .` refers to the Dockerfile location | |

<details>
<summary>Show Answers</summary>

| # | Statement | Answer |
|---|-----------|--------|
| 1 | Containers share the host operating system's kernel | **True** — Unlike VMs, containers don't include a full OS |
| 2 | Each Docker image contains a full copy of an operating system like a VM | **False** — Images contain only what's needed (libraries, app, deps), not a full OS |
| 3 | Docker layers are cached to speed up subsequent builds | **True** — Unchanged layers are reused from cache |
| 4 | When a container is removed, its data is preserved automatically | **False** — Container data is lost unless you use volumes |
| 5 | You can run multiple containers from a single image | **True** — One image, many container instances |
| 6 | The `.` in `docker build .` refers to the Dockerfile location | **False** — It refers to the build context (the directory sent to Docker), not the Dockerfile location |

</details>
