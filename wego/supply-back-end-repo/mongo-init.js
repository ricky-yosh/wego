// MongoDB initialization script
require('dotenv').config();
const databaseUser = process.env.DATABASE_USER;
const databasePassword = process.env.DATABASE_PASSWORD;
const databaseName = process.env.DATABASE_USER;

db.createUser({
    user: databaseUser,
    pwd: databasePassword,
    roles: [{ role: 'readWrite', db: databaseName }]
});