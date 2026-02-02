const express = require('express');
const router = express.Router();
const { v4: uuid } = require('uuid');

// Select persistence layer based on environment
const db = process.env.MYSQL_HOST
    ? require('../persistence/mysql')
    : require('../persistence/sqlite');

// Initialize the database
db.init().catch(err => {
    console.error('Failed to initialize database:', err);
    process.exit(1);
});

// GET all todos
router.get('/', async (req, res) => {
    try {
        const todos = await db.getAll();
        res.json(todos);
    } catch (err) {
        console.error('Error fetching todos:', err);
        res.status(500).json({ error: 'Failed to fetch todos' });
    }
});

// POST a new todo
router.post('/', async (req, res) => {
    try {
        const { title } = req.body;
        if (!title || title.trim() === '') {
            return res.status(400).json({ error: 'Title is required' });
        }
        const todo = {
            id: uuid(),
            title: title.trim(),
            completed: false
        };
        await db.create(todo);
        res.status(201).json(todo);
    } catch (err) {
        console.error('Error creating todo:', err);
        res.status(500).json({ error: 'Failed to create todo' });
    }
});

// PUT update a todo
router.put('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const { title, completed } = req.body;
        await db.update(id, { title, completed });
        res.json({ id, title, completed });
    } catch (err) {
        console.error('Error updating todo:', err);
        res.status(500).json({ error: 'Failed to update todo' });
    }
});

// DELETE a todo
router.delete('/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await db.remove(id);
        res.status(204).send();
    } catch (err) {
        console.error('Error deleting todo:', err);
        res.status(500).json({ error: 'Failed to delete todo' });
    }
});

module.exports = router;
