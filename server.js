const express = require("express");
const mysql = require("mysql");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public")); // Ensure your frontend still works

// MySQL Database Connection
const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "jubby2610", // If you set a MySQL password, add it here
    database: "shopDB"
});

// Connect to MySQL
db.connect((err) => {
    if (err) {
        console.error("Database connection failed:", err);
        return;
    }
    console.log("Connected to MySQL database");
});

// Test route to check if API is working
app.get("/", (req, res) => {
    res.send("API is running...");
});

// Route to get all products from the database
app.get("/apiproducts", (req, res) => {
    db.query("SELECT * FROM products", (err, results) => {
        if (err) {
            console.error("Error fetching products:", err);
            res.status(500).json({ error: "Database error" });
        } else {
            res.json(results);
        }
    });
});

// Route to get a single product by ID
app.get("/api/products/:id", (req, res) => {
    const productId = req.params.id;
    db.query("SELECT * FROM products WHERE id = ?", [productId], (err, result) => {
        if (err) {
            console.error("Error fetching product:", err);
            res.status(500).json({ error: "Database error" });
        } else {
            res.json(result[0] || {});
        }
    });
});

// Start Server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
