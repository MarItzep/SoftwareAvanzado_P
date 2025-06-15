require('dotenv').config();
const express = require('express');
const { Client } = require('pg');

const app = express();
const port = 3002;

const client = new Client({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 5432,
});

// coneccion del cliente
client.connect()
  .then(() => console.log('Conectado a la base de datos de pedidos'))
  .catch(err => console.error('Error al conectar a pedidos:', err));

app.use(express.json());

// get endpoint para verificar que el servicio está funcionando
app.get('/', (req, res) => {
  res.send(' Servicio de Pedidos en funcionamiento');
});
// get endpoint para obtener todos los pedidos

app.get('/pedidos', async (req, res) => {
  try {
    const result = await client.query('SELECT * FROM pedidos');
    res.json(result.rows);
  } catch (err) {
    res.status(500).send('Error al obtener pedidos');
  }
});

app.listen(port, () => {
  console.log(`Servicio de Pedidos corriendo en http://localhost:${port}`);
});
