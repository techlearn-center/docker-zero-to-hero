# Module 13 — Educational Resources

> **"The learning doesn't stop here."** This is a curated collection of resources to deepen your Docker knowledge and expand into related technologies.

---

## Official Documentation

| Resource | Link | Description |
|----------|------|-------------|
| Docker Docs | [docs.docker.com](https://docs.docker.com/) | The official reference — always start here |
| Dockerfile Reference | [docs.docker.com/reference/dockerfile](https://docs.docker.com/reference/dockerfile/) | Every Dockerfile instruction explained |
| Docker Compose Reference | [docs.docker.com/compose](https://docs.docker.com/compose/) | Complete Compose file specification |
| Docker Hub | [hub.docker.com](https://hub.docker.com/) | Browse official and community images |
| Docker CLI Reference | [docs.docker.com/reference/cli/docker](https://docs.docker.com/reference/cli/docker/) | Every command documented |

---

## Free Learning Paths

| Resource | Format | Level |
|----------|--------|-------|
| [Docker Getting Started Guide](https://docs.docker.com/get-started/) | Tutorial | Beginner |
| [Play with Docker](https://labs.play-with-docker.com/) | Interactive Lab | Beginner |
| [Docker Curriculum](https://docker-curriculum.com/) | Tutorial | Beginner-Intermediate |
| [KodeKloud Docker Free Labs](https://kodekloud.com/courses/docker-for-the-absolute-beginner/) | Video + Labs | Beginner |
| [Katacoda Docker Scenarios](https://killercoda.com/playgrounds/scenario/docker) | Interactive | Beginner-Intermediate |

---

## Books

| Book | Author | Best For |
|------|--------|----------|
| *Docker Deep Dive* | Nigel Poulton | Comprehensive Docker understanding |
| *Docker in Action* | Jeff Nickoloff | Practical Docker workflows |
| *The Docker Book* | James Turnbull | Beginners who prefer reading |
| *Docker Up & Running* | Sean Kane & Karl Matthias | Operations teams |
| *Kubernetes Up & Running* | Kelsey Hightower et al. | Next step after Docker |

---

## Video Courses

| Course | Platform | Duration |
|--------|----------|----------|
| Docker Mastery | Udemy (Bret Fisher) | ~20 hours |
| Docker & Kubernetes: The Practical Guide | Udemy (Maximilian Schwarzmuller) | ~24 hours |
| Docker for Developers | LinkedIn Learning | ~4 hours |
| Docker Essentials | Pluralsight | ~3 hours |

---

## YouTube Channels

| Channel | Content Style |
|---------|--------------|
| [TechWorld with Nana](https://www.youtube.com/@TechWorldwithNana) | Clear explanations, practical demos |
| [NetworkChuck](https://www.youtube.com/@NetworkChuck) | Fun, beginner-friendly |
| [Bret Fisher](https://www.youtube.com/@BretFisher) | Docker Captain, in-depth |
| [Fireship](https://www.youtube.com/@Fireship) | Quick overviews, "100 seconds" format |
| [DevOps Toolkit](https://www.youtube.com/@DevOpsToolkit) | Advanced DevOps topics |

---

## Cheat Sheets

We've included a Docker commands cheat sheet in this repo:

**[Docker Commands Cheat Sheet](../resources/cheatsheets/docker-commands.md)**

Other useful references:
- [Docker Cheat Sheet (GitHub)](https://github.com/wsargent/docker-cheat-sheet)
- [Docker Compose Cheat Sheet](https://devhints.io/docker-compose)

---

## Communities

| Community | Platform | Link |
|-----------|----------|------|
| Docker Community Forums | Forum | [forums.docker.com](https://forums.docker.com/) |
| Docker Slack | Chat | [dockercommunity.slack.com](https://dockercommunity.slack.com/) |
| r/docker | Reddit | [reddit.com/r/docker](https://www.reddit.com/r/docker/) |
| Stack Overflow | Q&A | [stackoverflow.com/questions/tagged/docker](https://stackoverflow.com/questions/tagged/docker) |
| Docker GitHub | Code | [github.com/docker](https://github.com/docker) |

---

## Related Technologies to Explore

Once you're comfortable with Docker, these technologies build on what you've learned:

```
                         Docker
                           │
              ┌────────────┼────────────┐
              │            │            │
         Kubernetes    CI/CD       Security
              │            │            │
         ┌────┴────┐  ┌───┴────┐  ┌───┴────────┐
         │         │  │        │  │            │
        Helm    Istio GitHub  Jenkins  Trivy   Falco
                      Actions
```

| Technology | What It Does | When to Learn |
|-----------|-------------|---------------|
| **Kubernetes** | Orchestrate containers at scale | After you're comfortable with Docker Compose |
| **Helm** | Package manager for Kubernetes | After Kubernetes basics |
| **GitHub Actions** | CI/CD pipelines | When you want to automate Docker builds |
| **Terraform** | Infrastructure as Code | When you deploy to cloud |
| **Prometheus + Grafana** | Monitor containers | When running containers in production |
| **Trivy / Snyk** | Scan images for vulnerabilities | Before deploying to production |

---

## Certifications

| Certification | Provider | Level |
|--------------|----------|-------|
| Docker Certified Associate (DCA) | Docker/Mirantis | Intermediate |
| Certified Kubernetes Administrator (CKA) | CNCF | Intermediate |
| AWS Certified Solutions Architect | AWS | Intermediate |

---

## Final Words

You've completed the Docker Zero-to-Hero workshop! Here's what we suggest:

1. **Practice** — Containerize your own projects
2. **Explore** — Try different base images, languages, and architectures
3. **Build** — Set up a CI/CD pipeline that builds Docker images
4. **Scale** — Learn Kubernetes for container orchestration
5. **Share** — Help others learn Docker — teaching is the best way to master it

---

**[Back to Workshop Home](../README.md)**
