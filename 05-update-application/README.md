# Module 05 — Update the Application (10 pts)

> **"Software is never done."** In this module, you'll change the app's source code, rebuild the image, and learn an important lesson about Docker's ephemeral nature.

---

## What You'll Learn

- How to update source code and rebuild an image
- Why you need to stop/remove old containers before starting new ones
- That containers are **ephemeral** — data doesn't persist by default
- How layer caching speeds up rebuilds

---

## Step 1 — Make a Change

Open `app/src/static/index.html` and change the empty state text.

**Find this line:**

```html
No todos yet! Add one above to get started.
```

**Change it to something different**, for example:

```html
You have no todos yet! Add your first task above.
```

This is a small change, but it proves you can modify the app and ship an update.

---

## Step 2 — Rebuild the Image

```bash
cd app
docker build -t todo-app .
```

Notice how fast the rebuild is! Docker uses cached layers:

```
[+] Building 2.1s (10/10) FINISHED
 => CACHED [1/5] FROM node:18-alpine          ← Cached!
 => CACHED [2/5] WORKDIR /app                 ← Cached!
 => CACHED [3/5] COPY package.json .          ← Cached!
 => CACHED [4/5] RUN npm install --production ← Cached!
 => [5/5] COPY . .                            ← Rebuilt (code changed)
```

Only the `COPY . .` layer and above are rebuilt because only the source code changed — `package.json` is the same, so `npm install` is cached.

---

## Step 3 — Handle the Old Container

Try running the new container:

```bash
docker run -dp 3000:3000 todo-app
```

**Error!** You'll see something like:

```
docker: Error response from daemon: driver failed...: Bind for 0.0.0.0:3000 failed:
port is already allocated.
```

### Why?

The old container is still running on port 3000. You can't have two containers on the same port.

### Fix It — Stop and Remove the Old Container

```bash
# Find the old container
docker ps

# Stop it
docker stop <container-id>

# Remove it
docker rm <container-id>

# Or do both in one command
docker rm -f <container-id>
```

### Now Start the New Container

```bash
docker run -dp 3000:3000 todo-app
```

Visit http://localhost:3000 — you should see your updated text!

---

## Step 4 — Notice the Data Loss

Here's the key lesson:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Old container had todos → GONE after docker rm     │
│   New container starts fresh → Empty todo list       │
│                                                      │
│   Containers are EPHEMERAL                           │
│   Their filesystem dies with them                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

If you added todos in Module 04, they're now gone. The new container starts with a fresh database.

**This is by design** — and we'll fix it in Module 07 with **volumes**.

---

## The Update Workflow

Here's the pattern you'll follow every time you update your app:

```
  Edit Code → Build Image → Stop Old Container → Start New Container

  ┌──────┐     ┌──────┐     ┌──────────┐     ┌──────────┐
  │ Edit │────→│Build │────→│ Stop/Rm  │────→│ Run New  │
  │ code │     │image │     │ old      │     │container │
  └──────┘     └──────┘     └──────────┘     └──────────┘
```

In production, tools like Kubernetes handle this automatically (rolling updates). For now, we do it manually to understand the process.

---

## Progressive Hints

<details>
<summary>💡 Hint 1 — Where to make the change</summary>

Edit the file `app/src/static/index.html`. Look for the `<p>` tag with `id="empty-state"`.

</details>

<details>
<summary>💡 Hint 2 — Common mistake</summary>

Make sure to rebuild from the `app/` directory:
```bash
cd app
docker build -t todo-app .
```

And don't forget to stop the old container before starting the new one!

</details>

<details>
<summary>💡 Hint 3 — Full update sequence</summary>

```bash
# 1. Edit app/src/static/index.html (change the empty state text)

# 2. Rebuild
cd app
docker build -t todo-app .

# 3. Stop and remove old container
docker rm -f $(docker ps -q --filter ancestor=todo-app)

# 4. Run new container
docker run -dp 3000:3000 todo-app
```

</details>

---

## Grading Criteria (10 pts)

| Check | Points | What's Verified |
|-------|--------|-----------------|
| Source modified | 5 | The empty state text in `index.html` has been changed |
| Image rebuilds | 5 | `docker build` succeeds with the updated code |

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] You changed the empty state text in `app/src/static/index.html`
- [ ] `docker build -t todo-app .` rebuilds successfully
- [ ] The new container shows your updated text at http://localhost:3000
- [ ] You understand why the old todos were lost
- [ ] `python run.py --module 05` scores 10/10

---

**Next up:** [Module 06 — Share the Application](../06-share-application/README.md) — Push your image to Docker Hub so anyone can use it.
