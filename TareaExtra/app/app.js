const express = require("express");
const { sequelize } = require("./models");
const authRoutes = require("./routes/authroutes");
require("dotenv").config();

const app = express();
app.use(express.json());
app.use("/api/auth", authRoutes);

const PORT = 4000;
app.listen(PORT, async () => {
  console.log(`Servidor en puerto ${PORT}`);
  try {
    await sequelize.sync({ force: false });
    console.log("Conectado a la base de datos.");
  } catch (err) {
    console.error("Error al conectar la base de datos:", err);
  }
});
