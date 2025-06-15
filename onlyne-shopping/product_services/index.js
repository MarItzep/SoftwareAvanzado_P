require('dotenv').config();
const express = require('express');
const { Client } = require('pg');

const app = express();
const port = 3001;

const client = new Client({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 5432,
});

client.connect()
  .then(() => console.log(' Conectado a la base de datos de productos'))
  .catch(err => console.error(' Error al conectar a productos:', err));

app.use(express.json());

app.get('/', (req, res) => {
  res.send(' Servicio de Productos en funcionamiento');
});


app.get('/productos', async (req, res) => {
  try {
    const result = await client.query('SELECT * FROM productos');
    res.json(result.rows);
  } catch (err) {
    res.status(500).send('Error al obtener productos');
  }
});

app.listen(port, () => {
  console.log(`Servicio de Productos corriendo en http://localhost:${port}`);
});
