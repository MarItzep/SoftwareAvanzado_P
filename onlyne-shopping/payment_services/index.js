require('dotenv').config();
const express = require('express');
const { Client } = require('pg');

const app = express();
const port = 3003;

const client = new Client({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: 5432,
});

// Conexión del cliente a la base de datos de pagos
client.connect()
  .then(() => console.log('💳 Conectado a la base de datos de pagos'))
  .catch(err => console.error('Error al conectar a pagos:', err));

  
app.use(express.json());
// Endpoint para verificar que el servicio está funcionando
app.get('/', (req, res) => {
  res.send('💳 Servicio de Pagos en funcionamiento');
});

// Endpoint para procesar un pago
app.get('/pagos', async (req, res) => {
  try {
    const result = await client.query('SELECT * FROM pagos');
    res.json(result.rows);
  } catch (err) {
    res.status(500).send('Error al obtener pagos');
  }
});

app.listen(port, () => {
  console.log(`Servicio de Pagos corriendo en http://localhost:${port}`);
});
