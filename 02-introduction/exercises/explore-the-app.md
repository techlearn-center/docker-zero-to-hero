# Exercise: Explore the Todo App

Before we containerize the app, let's understand how it works. Open the files listed below and answer each question.

---

### Part 1 — The Server (`app/src/index.js`)

Open `app/src/index.js` and answer:

**Q1:** What port does the Express server listen on?

<details>
<summary>Answer</summary>

Port **3000** (or the value of the `TODO_PORT` environment variable if set).

```javascript
const PORT = process.env.TODO_PORT || 3000;
```

</details>

**Q2:** What directory is used to serve static files (HTML, CSS, JS)?

<details>
<summary>Answer</summary>

`src/static` — The server uses `express.static()` to serve files from the `static` subdirectory.

</details>

---

### Part 2 — The Routes (`app/src/routes/todos.js`)

Open `app/src/routes/todos.js` and answer:

**Q3:** What four CRUD operations does the API support? List the HTTP method and path for each.

<details>
<summary>Answer</summary>

| Operation | Method | Path |
|-----------|--------|------|
| List all | GET | `/` |
| Create | POST | `/` |
| Update | PUT | `/:id` |
| Delete | DELETE | `/:id` |

These are mounted at `/api/todos` in `index.js`.

</details>

**Q4:** How does the app decide whether to use SQLite or MySQL?

<details>
<summary>Answer</summary>

It checks if the `MYSQL_HOST` environment variable is set:

```javascript
if (process.env.MYSQL_HOST) {
    db = require('../persistence/mysql');
} else {
    db = require('../persistence/sqlite');
}
```

If `MYSQL_HOST` is set → MySQL. Otherwise → SQLite.

</details>

---

### Part 3 — The Persistence Layer (`app/src/persistence/sqlite.js`)

Open `app/src/persistence/sqlite.js` and answer:

**Q5:** Where does SQLite store its database file inside the container?

<details>
<summary>Answer</summary>

At the path specified by `SQLITE_DB_PATH` environment variable, or defaults to `../../data/todos.db` relative to the script file (which resolves to `/app/data/todos.db` inside the container).

This path is important — in Module 07, you'll mount a volume at `/app/data` to persist the database.

</details>

---

### Part 4 — The Frontend (`app/src/static/index.html`)

Open `app/src/static/index.html` and answer:

**Q6:** What text is shown when the todo list is empty?

<details>
<summary>Answer</summary>

"No todos yet! Add one above to get started."

In Module 05, you'll change this text and rebuild the image to practice the update workflow.

</details>

---

### Part 5 — The Package (`app/package.json`)

Open `app/package.json` and answer:

**Q7:** What are the three main dependencies (not devDependencies)?

<details>
<summary>Answer</summary>

1. **express** — Web framework
2. **mysql2** — MySQL database driver
3. **sqlite3** — SQLite database driver
4. **uuid** — For generating unique todo IDs

(There are four, but the three database/server dependencies are express, mysql2, and sqlite3.)

</details>

**Q8:** What command starts the development server with auto-restart?

<details>
<summary>Answer</summary>

```bash
npm run dev
```

This runs `nodemon src/index.js`, which watches for file changes and automatically restarts the server. You'll use this in Module 08 with bind mounts.

</details>

---

### Summary

Now you know:
- The server runs on port **3000**
- It switches between **SQLite** and **MySQL** based on the `MYSQL_HOST` env var
- SQLite stores data at `/app/data/todos.db` (important for volumes!)
- The app has a simple CRUD API at `/api/todos`
- `nodemon` is available for development auto-reloading

This knowledge will be essential when you write the Dockerfile in Module 04.
