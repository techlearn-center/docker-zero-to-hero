# Module 06 — Share the Application (10 pts)

> **"What good is a lunchbox if you can't share it?"** In this module, you'll learn how to push your Docker image to Docker Hub so anyone (or any server) can pull and run it.

---

## What You'll Learn

- How Docker image naming and tagging works
- How to push an image to Docker Hub
- How to pull and run an image from Docker Hub
- The difference between `latest` and specific tags

---

## Step 1 — Create a Docker Hub Account

If you don't have one already:

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for a free account
3. Remember your **username** — you'll need it for tagging

---

## Step 2 — Log In from the CLI

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

```
Login Succeeded
```

---

## Step 3 — Understand Image Tags

Docker images follow this naming convention:

```
  registry / username / repository : tag

  docker.io / myuser  / todo-app  : 1.0
  ────────   ────────   ────────    ───
  (default)  (yours)   (image)    (version)
```

When you built `todo-app` earlier, the full name was actually:

```
docker.io/library/todo-app:latest
```

To push to YOUR Docker Hub, you need to tag it with YOUR username:

```
docker.io/YOUR_USERNAME/todo-app:1.0
```

---

## Step 4 — Tag Your Image

Replace `YOUR_USERNAME` with your Docker Hub username:

```bash
docker tag todo-app YOUR_USERNAME/todo-app:1.0
```

This doesn't create a new image — it creates an **alias** (like a symlink):

```
todo-app:latest ──────┐
                      ├──→ Same image (same ID)
YOUR_USERNAME/todo-app:1.0 ─┘
```

Verify:

```bash
docker images | grep todo-app
```

You should see both names pointing to the same image ID.

---

## Step 5 — Push to Docker Hub

```bash
docker push YOUR_USERNAME/todo-app:1.0
```

You'll see each layer being pushed:

```
The push refers to repository [docker.io/YOUR_USERNAME/todo-app]
5f70bf18a086: Pushed
a1b2c3d4e5f6: Pushed
...
1.0: digest: sha256:abc123... size: 1234
```

### View It Online

Visit: `https://hub.docker.com/r/YOUR_USERNAME/todo-app`

Your image is now available to anyone!

---

## Step 6 — Pull and Run (Simulate a Fresh Machine)

To prove it works, let's simulate pulling on a "new machine":

```bash
# Remove local images
docker rmi todo-app
docker rmi YOUR_USERNAME/todo-app:1.0

# Pull from Docker Hub
docker pull YOUR_USERNAME/todo-app:1.0

# Run it
docker run -dp 3000:3000 YOUR_USERNAME/todo-app:1.0
```

Visit http://localhost:3000 — the app works, pulled entirely from Docker Hub!

---

## Understanding Tags

```
YOUR_USERNAME/todo-app:1.0      ← Specific version (recommended)
YOUR_USERNAME/todo-app:latest   ← "Latest" tag (default, can be confusing)
YOUR_USERNAME/todo-app:dev      ← Custom tag for development
YOUR_USERNAME/todo-app:prod     ← Custom tag for production
```

### Best Practice: Always Use Specific Tags

```
BAD:                              GOOD:
FROM node:latest                  FROM node:18-alpine
docker push myapp:latest          docker push myapp:1.0

Why? "latest" can change           Specific tags are immutable
without warning                    and reproducible
```

---

## The Push/Pull Workflow

```
  Developer A                Docker Hub               Developer B
  ┌──────────┐              ┌──────────┐              ┌──────────┐
  │          │   push       │          │   pull       │          │
  │  Build   │─────────────→│  Store   │─────────────→│  Run     │
  │  & Tag   │              │  Image   │              │  Same    │
  │          │              │          │              │  Image!  │
  └──────────┘              └──────────┘              └──────────┘
```

This is how containerized applications are distributed — build once, run anywhere.

---

## Progressive Hints

<details>
<summary>💡 Hint 1 — Naming convention</summary>

The format is: `docker tag SOURCE_IMAGE USERNAME/IMAGE_NAME:TAG`

Replace `YOUR_USERNAME` with your actual Docker Hub username.

</details>

<details>
<summary>💡 Hint 2 — Common issues</summary>

- **"denied: requested access to the resource is denied"** → Make sure you ran `docker login` first
- **"tag does not exist"** → Make sure the source image name matches exactly
- **Image name must be lowercase** → Docker Hub usernames are always lowercase

</details>

<details>
<summary>💡 Hint 3 — Full sequence</summary>

```bash
# Log in
docker login

# Tag (replace YOUR_USERNAME)
docker tag todo-app YOUR_USERNAME/todo-app:1.0

# Push
docker push YOUR_USERNAME/todo-app:1.0

# Verify on Docker Hub
# Visit: https://hub.docker.com/r/YOUR_USERNAME/todo-app
```

</details>

---

## Grading Criteria (10 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Image tagged correctly | 5 | Image has a tag in `username/repo:tag` format |
| Push-ready image | 5 | Tagged image exists locally |

> **Note:** The auto-grader checks that you've tagged the image correctly. It does not require an actual push to Docker Hub (since that requires authentication).

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You have a Docker Hub account
- [ ] `docker login` succeeded
- [ ] You tagged the image: `docker tag todo-app YOUR_USERNAME/todo-app:1.0`
- [ ] You pushed the image: `docker push YOUR_USERNAME/todo-app:1.0`
- [ ] `python run.py --module 06` scores 10/10

---

**Next up:** [Module 07 — Persist the DB](../07-persist-the-db/README.md) — Solve the data loss problem with Docker volumes.
