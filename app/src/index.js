const express = require('express');
const path = require('path');
const todoRoutes = require('./routes/todos');
const healthRoutes = require('./routes/health');

const app = express();
const PORT = process.env.TODO_PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, 'static')));

// Routes
app.use('/api/todos', todoRoutes);
app.use('/', healthRoutes);

// Start server
app.listen(PORT, () => {
    console.log(`Todo app listening on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Persistence: ${process.env.MYSQL_HOST ? 'MySQL' : 'SQLite'}`);
});

module.exports = app;
