const mysql = require('mysql2/promise');

let pool;

function getPool() {
    if (!pool) {
        pool = mysql.createPool({
            host: process.env.MYSQL_HOST || 'localhost',
            user: process.env.MYSQL_USER || 'root',
            password: process.env.MYSQL_PASSWORD || 'secret',
            database: process.env.MYSQL_DB || 'todos',
            waitForConnections: true,
            connectionLimit: 10,
            queueLimit: 0
        });
    }
    return pool;
}

module.exports = {
    async init() {
        const p = getPool();
        await p.query(
            `CREATE TABLE IF NOT EXISTS todos (
                id VARCHAR(36) PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN DEFAULT false
            )`
        );
    },

    async getAll() {
        const p = getPool();
        const [rows] = await p.query('SELECT * FROM todos ORDER BY title');
        return rows.map(r => ({ ...r, completed: !!r.completed }));
    },

    async create(todo) {
        const p = getPool();
        await p.query(
            'INSERT INTO todos (id, title, completed) VALUES (?, ?, ?)',
            [todo.id, todo.title, todo.completed]
        );
        return todo;
    },

    async update(id, updates) {
        const p = getPool();
        const fields = [];
        const values = [];
        if (updates.title !== undefined) {
            fields.push('title = ?');
            values.push(updates.title);
        }
        if (updates.completed !== undefined) {
            fields.push('completed = ?');
            values.push(updates.completed);
        }
        values.push(id);
        await p.query(`UPDATE todos SET ${fields.join(', ')} WHERE id = ?`, values);
    },

    async remove(id) {
        const p = getPool();
        await p.query('DELETE FROM todos WHERE id = ?', [id]);
    }
};
