# Troubleshooting Guide

Common issues and their solutions, organized by topic.

---

## Docker Installation & Startup

### "docker: command not found"

**Cause:** Docker CLI is not installed or not in your PATH.

**Fix:**
- **macOS/Windows:** Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
- **Linux:** Follow the installation steps in Module 00
- **Windows:** Make sure Docker Desktop is running (whale icon in system tray)

### "Cannot connect to the Docker daemon"

**Cause:** Docker Desktop is not running.

**Fix:**
- **macOS:** Launch Docker Desktop from Applications
- **Windows:** Launch Docker Desktop from the Start menu and wait for the whale icon
- **Linux:** Start the service:
  ```bash
  sudo systemctl start docker
  ```

### "permission denied" (Linux)

**Cause:** Your user is not in the `docker` group.

**Fix:**
```bash
sudo usermod -aG docker $USER
# Then log out and log back in (or run: newgrp docker)
```

---

## Building Images

### "COPY failed: file not found"

**Cause:** The file you're trying to COPY doesn't exist in the build context.

**Fix:**
- Make sure you're running `docker build` from the correct directory
- Check that the file path in COPY matches the actual file location
- Remember: the build context is the directory you pass to `docker build` (the `.` in `docker build .`)

### Build is slow every time

**Cause:** Layer caching isn't being used effectively.

**Fix:** Reorder your Dockerfile:
```dockerfile
# Copy dependency manifest first
COPY package.json .
RUN npm install --production
# THEN copy source code
COPY . .
```

See Module 11 and the layer ordering exercise in Module 03.

### "no space left on device"

**Cause:** Docker's storage is full.

**Fix:**
```bash
# See what's using space
docker system df

# Clean up unused images, containers, networks
docker system prune

# Nuclear option: clean EVERYTHING (including unused images)
docker system prune -a
```

---

## Running Containers

### "port is already allocated"

**Cause:** Another container (or process) is already using that port.

**Fix:**
```bash
# Find what's using the port
docker ps  # Check for containers on port 3000

# Stop the old container
docker rm -f <container-id>

# Or use a different port
docker run -dp 3001:3000 todo-app  # Maps host:3001 to container:3000
```

### Container exits immediately

**Cause:** The app inside the container is crashing.

**Fix:**
```bash
# Check the logs
docker logs <container-id>

# Run interactively to debug
docker run -it todo-app sh

# Check if the CMD is correct
docker inspect todo-app --format='{{.Config.Cmd}}'
```

### "exec format error"

**Cause:** The image was built for a different CPU architecture (e.g., ARM image on x86).

**Fix:**
```bash
# Build for your platform explicitly
docker build --platform linux/amd64 -t todo-app .
```

---

## Volumes & Data

### "No such file or directory" with volumes

**Cause:** The mount path inside the container doesn't exist.

**Fix:** Make sure `WORKDIR` creates the directory, or the app creates it at startup. The volume mount creates the mount point, but the directory structure inside must be correct.

### Data not persisting between container restarts

**Cause:** Not using a named volume.

**Fix:**
```bash
# This DOES NOT persist (anonymous, removed with container):
docker run todo-app

# This DOES persist (named volume):
docker run -v todo-db:/app/data todo-app
```

### Bind mount shows empty directory

**Cause:** On macOS/Windows, the directory isn't shared with Docker Desktop.

**Fix:**
- Docker Desktop > Settings > Resources > File Sharing
- Make sure the parent directory of your project is listed

---

## Networking

### Containers can't communicate

**Cause:** Containers are not on the same Docker network.

**Fix:**
```bash
# Create a network
docker network create todo-network

# Run BOTH containers on it
docker run --network todo-network --name mysql ...
docker run --network todo-network --name todo-app ...
```

### "Name resolution failure" / can't reach MySQL

**Cause:** Using wrong hostname. Container names are used as hostnames on Docker networks.

**Fix:**
- Set `MYSQL_HOST` to the **container name** (e.g., `mysql`), not `localhost` or an IP
- Both containers must be on the same network
- MySQL might not be ready yet — wait 10-15 seconds after starting MySQL

---

## Docker Compose

### "no configuration file provided"

**Cause:** No `docker-compose.yml` in the current directory.

**Fix:** Run `docker compose` from the directory containing `docker-compose.yml`:
```bash
ls docker-compose.yml  # Verify it exists
docker compose up -d
```

### "service web depends on mysql which is undefined"

**Cause:** Typo in service name or `depends_on` reference.

**Fix:** Make sure the service names match exactly:
```yaml
services:
  web:
    depends_on:
      - mysql    # Must match exactly
  mysql:         # This name
    image: mysql:8.0
```

### MySQL connection refused on startup

**Cause:** The app starts before MySQL is fully initialized. `depends_on` only waits for the container to **start**, not for MySQL to be **ready**.

**Fix:** Add retry logic or a wait script. Quick workaround:
```bash
# Start just MySQL first
docker compose up -d mysql
# Wait a moment
sleep 10
# Then start the app
docker compose up -d web
```

---

## Windows-Specific Issues

### WSL 2 not installed

**Cause:** Docker Desktop requires WSL 2 on Windows.

**Fix:**
```powershell
# Open PowerShell as Administrator
wsl --install
# Restart your computer
```

### Path issues with bind mounts

**Cause:** Windows paths use backslashes, Docker expects forward slashes.

**Fix:** Use PowerShell variable `${PWD}` instead of `$(pwd)`:
```powershell
docker run -v "${PWD}/app:/app" todo-app
```

### Line ending issues (CRLF vs LF)

**Cause:** Windows uses CRLF line endings, Linux containers expect LF.

**Fix:** Add to your `.gitattributes`:
```
* text=auto eol=lf
```

Or configure your editor to use LF line endings for Dockerfiles and shell scripts.

---

## Getting More Help

1. Check the [Docker documentation](https://docs.docker.com/)
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/docker)
3. Review the module README for specific guidance
4. Run the module's `verify.sh` script for quick diagnostics
5. Run `python run.py --module <number>` for grading feedback
