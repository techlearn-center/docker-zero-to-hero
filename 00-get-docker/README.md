# Module 00 — Get Docker

> **"You can't sail without a ship."** Before we containerize anything, let's get Docker installed and verified on your machine.

---

## What You'll Do

| Step | Action | Time |
|------|--------|------|
| 1 | Install Docker Desktop (or Docker Engine) | ~5 min |
| 2 | Verify the installation | ~1 min |
| 3 | Run your first container | ~1 min |

---

## Step 1 — Install Docker

Pick your operating system:

<details>
<summary><strong>🖥️ macOS</strong></summary>

1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download **Docker Desktop for Mac**
   - Apple Silicon (M1/M2/M3)? Choose the **Apple chip** version
   - Intel Mac? Choose the **Intel chip** version
3. Open the `.dmg` file and drag Docker to Applications
4. Launch Docker Desktop from Applications
5. Wait for the whale icon in the menu bar to stop animating

</details>

<details>
<summary><strong>🪟 Windows</strong></summary>

1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Download **Docker Desktop for Windows**
3. Run the installer (requires admin privileges)
4. **Important:** Enable WSL 2 backend when prompted (recommended)
5. Restart your computer if prompted
6. Launch Docker Desktop from the Start menu
7. Wait for the whale icon in the system tray to indicate "Docker is running"

> **WSL 2 Tip:** If you don't have WSL 2, Docker Desktop will prompt you to install it. Follow the on-screen instructions or visit [Microsoft's WSL install guide](https://learn.microsoft.com/en-us/windows/wsl/install).

</details>

<details>
<summary><strong>🐧 Linux (Ubuntu/Debian)</strong></summary>

```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Set up the repository
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group (no sudo needed for docker commands)
sudo usermod -aG docker $USER
newgrp docker
```

</details>

---

## Step 2 — Verify the Installation

Open a terminal and run:

```bash
docker --version
```

You should see something like:

```
Docker version 24.x.x, build xxxxxxx
```

Also check Docker Compose:

```bash
docker compose version
```

Expected output:

```
Docker Compose version v2.x.x
```

---

## Step 3 — Run Your First Container

```bash
docker run hello-world
```

If everything is working, you'll see:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### What Just Happened?

```
┌─────────────────────────────────────────────────┐
│  You typed: docker run hello-world              │
│                                                 │
│  1. Docker looked for "hello-world" locally     │
│  2. Didn't find it → pulled from Docker Hub     │
│  3. Created a container from that image         │
│  4. Ran the container (printed the message)     │
│  5. Container exited                            │
└─────────────────────────────────────────────────┘
```

Don't worry if this doesn't fully make sense yet — we'll break down every concept in the upcoming modules.

---

## Troubleshooting

<details>
<summary><strong>❌ "docker: command not found"</strong></summary>

- **macOS/Windows:** Make sure Docker Desktop is running (check for the whale icon)
- **Linux:** Make sure you completed the installation steps and started the service:
  ```bash
  sudo systemctl start docker
  ```

</details>

<details>
<summary><strong>❌ "permission denied" on Linux</strong></summary>

You need to add your user to the `docker` group:
```bash
sudo usermod -aG docker $USER
```
Then **log out and log back in** (or run `newgrp docker`).

</details>

<details>
<summary><strong>❌ "Cannot connect to the Docker daemon"</strong></summary>

Docker Desktop might not be running. Start it and wait for the whale icon to indicate it's ready.

</details>

---

## Checkpoint ✅

Before moving on, confirm:

- [ ] `docker --version` returns a version number
- [ ] `docker compose version` returns a version number
- [ ] `docker run hello-world` prints the success message

---

**Ready?** Head to [Module 01 — What is Docker?](../01-what-is-docker/README.md)
