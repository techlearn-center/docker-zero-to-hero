# Exercise: Dockerfile Layer Ordering

## The Challenge

Below is a Dockerfile that works but is **poorly optimized**. Every time you change your source code, Docker has to reinstall all dependencies — even if `package.json` hasn't changed.

### The Bad Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install --production
EXPOSE 3000
CMD ["node", "src/index.js"]
```

### Your Task

Rewrite this Dockerfile so that:
1. Dependencies (`npm install`) are **cached** when only source code changes
2. The build is as fast as possible for typical code-only changes
3. All instructions are in the optimal order

**Hint:** Think about which files change most frequently and which change rarely.

---

### Write Your Answer Here

```dockerfile
FROM node:18-alpine
WORKDIR /app
# TODO: Reorder the COPY and RUN instructions for optimal caching
```

---

<details>
<summary>Show Optimized Solution</summary>

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "src/index.js"]
```

### Why This Order?

```
Instruction              Changes when...          Cache impact
─────────────────────────────────────────────────────────────
FROM node:18-alpine      Almost never             Always cached
WORKDIR /app             Almost never             Always cached
COPY package.json .      Dependencies change      Rarely busted
RUN npm install          Dependencies change      Rarely busted
COPY . .                 Any code change          Frequently busted
EXPOSE 3000              Almost never             Rebuilt (above changed)
CMD [...]                Almost never             Rebuilt (above changed)
```

**Key insight:** Copy `package.json` FIRST, install dependencies, THEN copy the rest of the code. This way, `npm install` only re-runs when `package.json` changes — not on every code edit.

</details>

---

## Bonus Challenge

Here's a Python Dockerfile with the same problem. Can you optimize it?

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
```

<details>
<summary>Show Optimized Solution</summary>

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

Same principle: copy the dependency manifest (`requirements.txt`) first, install, then copy the rest.

This pattern applies to **every language**:
- Node.js: `package.json` → `npm install` → `COPY . .`
- Python: `requirements.txt` → `pip install` → `COPY . .`
- Go: `go.mod` + `go.sum` → `go mod download` → `COPY . .`
- Java: `pom.xml` → `mvn dependency:resolve` → `COPY . .`

</details>
