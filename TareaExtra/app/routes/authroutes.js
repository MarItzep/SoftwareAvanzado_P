const express = require("express");
const router = express.Router();
const authController = require("../controllers/authcontroller");
const authMiddleware = require("../middlewares/authMiddleware");

// Endpoint para registrar un nuevo usuario
router.post("/register", authController.register);

// Endpoint para iniciar sesión
router.post("/login", authController.login);

// Endpoint protegido: requiere token JWT
router.get("/profile", authMiddleware, (req, res) => {
  res.json({ message: "Perfil accedido correctamente", user: req.user });
});

module.exports = router;
