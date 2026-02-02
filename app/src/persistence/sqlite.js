const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = process.env.SQLITE_DB_PATH || path.join(__dirname, '../../data/todos.db');
let db;

function getDb() {
    if (!db) {
        const fs = require('fs');
        const dir = path.dirname(DB_PATH);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        db = new sqlite3.Database(DB_PATH);
    }
    return db;
}

module.exports = {
    async init() {
        const database = getDb();
        return new Promise((resolve, reject) => {
            database.run(
                `CREATE TABLE IF NOT EXISTS todos (
                    id VARCHAR(36) PRIMARY KEY,
                    title TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0
                )`,
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    },

    async getAll() {
        const database = getDb();
        return new Promise((resolve, reject) => {
            database.all('SELECT * FROM todos ORDER BY rowid DESC', (err, rows) => {
                if (err) reject(err);
                else resolve(rows.map(r => ({ ...r, completed: !!r.completed })));
            });
        });
    },

    async create(todo) {
        const database = getDb();
        return new Promise((resolve, reject) => {
            database.run(
                'INSERT INTO todos (id, title, completed) VALUES (?, ?, ?)',
                [todo.id, todo.title, todo.completed ? 1 : 0],
                (err) => {
                    if (err) reject(err);
                    else resolve(todo);
                }
            );
        });
    },

    async update(id, updates) {
        const database = getDb();
        const fields = [];
        const values = [];
        if (updates.title !== undefined) {
            fields.push('title = ?');
            values.push(updates.title);
        }
        if (updates.completed !== undefined) {
            fields.push('completed = ?');
            values.push(updates.completed ? 1 : 0);
        }
        values.push(id);
        return new Promise((resolve, reject) => {
            database.run(
                `UPDATE todos SET ${fields.join(', ')} WHERE id = ?`,
                values,
                (err) => {
                    if (err) reject(err);
                    else resolve();
                }
            );
        });
    },

    async remove(id) {
        const database = getDb();
        return new Promise((resolve, reject) => {
            database.run('DELETE FROM todos WHERE id = ?', [id], (err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    }
};
