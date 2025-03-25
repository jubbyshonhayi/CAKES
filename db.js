const mysql = require('mysql2');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',      // Change if you set a different username
    password: 'jubby2610',      // Add your password if you set one
    database: 'shopDB'
});

// Test the connection
connection.connect((err) => {
    if (err) {
        console.error('Database connection failed:', err);
        return;
    }
    console.log('Connected to MySQL Database!');
});

module.exports = connection;
