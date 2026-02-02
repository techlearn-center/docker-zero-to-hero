const express = require('express');
const router = express.Router();

router.get('/healthz', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        persistence: process.env.MYSQL_HOST ? 'mysql' : 'sqlite'
    });
});

module.exports = router;
