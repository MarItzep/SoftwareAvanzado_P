# Manual de Sistema de Autenticación - Vibe Coding

## 📋 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Arquitectura del Sistema](#️-arquitectura-del-sistema)
3. [Configuración del Proyecto](#-configuración-del-proyecto)
4. [Estructura de Archivos](#-estructura-de-archivos)
5. [API Endpoints](#-api-endpoints)
6. [Casos de Uso](#-casos-de-uso)
7. [Documentación de Prompts](#-documentación-de-prompts)
8. [Seguridad](#-seguridad)
9. [Troubleshooting](#️-troubleshooting)
10. [Referencias](#-referencias)
11. [Soporte](#-soporte)

---

## 🎯 Descripción General

Este sistema de autenticación implementa un flujo completo de registro e inicio de sesión utilizando Node.js, Express, Sequelize (PostgreSQL) y JWT (JSON Web Tokens). El sistema proporciona endpoints RESTful para la gestión de usuarios con autenticación segura.

### Tecnologías Utilizadas
- **Backend**: Node.js + Express.js
- **Base de Datos**: PostgreSQL con Sequelize ORM
- **Autenticación**: JWT (JSON Web Tokens)
- **Encriptación**: bcrypt para hash de contraseñas
- **Variables de Entorno**: dotenv

---

## 🏗️ Arquitectura del Sistema

```
app/
├── app.js                 # Punto de entrada de la aplicación
├── models/
│   ├── index.js          # Configuración de Sequelize
│   └── User.js           # Modelo de Usuario
├── controllers/
│   └── authcontroller.js # Lógica de autenticación
├── routes/
│   └── authroutes.js     # Definición de rutas
└── middlewares/
    └── authMiddleware.js # Middleware de autenticación
```

---

## ⚙️ Configuración del Proyecto

### Variables de Entorno (.env)
```env
DB_NAME=nombre_base_datos
DB_USER=usuario_base_datos
DB_PASSWORD=contraseña_base_datos
DB_HOST=localhost
DB_PORT=5432
```

### Dependencias Requeridas
```json
{
  "express": "^4.18.0",
  "sequelize": "^6.0.0",
  "pg": "^8.0.0",
  "jsonwebtoken": "^9.0.0",
  "bcrypt": "^5.0.0",
  "dotenv": "^16.0.0"
}
```

---

## 📁 Estructura de Archivos

### 1. `app.js` - Punto de Entrada
```javascript
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
```

### 2. `models/User.js` - Modelo de Usuario
```javascript
const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
  const User = sequelize.define("User", {
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      validate: { isEmail: true },
    },
    password: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  });

  return User;
};
```

### 3. `controllers/authcontroller.js` - Controlador de Autenticación
```javascript
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const { User } = require("../models");

exports.register = async (req, res) => {
  const { email, password } = req.body;
  const hashed = await bcrypt.hash(password, 10);
  const user = await User.create({ email, password: hashed });
  res.status(201).json({ message: "User created", user });
};

exports.login = async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ where: { email } });
  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.status(401).json({ error: "Invalid credentials" });
  const token = jwt.sign({ id: user.id }, "secretkey", { expiresIn: "1h" });
  res.json({ token });
};
```

### 4. `middlewares/authMiddleware.js` - Middleware de Autenticación
```javascript
const jwt = require("jsonwebtoken");

module.exports = (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(403).json({ error: "Token required" });

  try {
    const data = jwt.verify(token, "secretkey");
    req.user = data;
    next();
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
};
```

---

## 🔗 API Endpoints

### Base URL: `http://localhost:4000/api/auth`

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/register` | Registrar nuevo usuario | No |
| POST | `/login` | Iniciar sesión | No |
| GET | `/profile` | Obtener perfil del usuario | Sí (JWT) |

---

## 📝 Casos de Uso

### Caso de Uso 1: Registro de Usuario

**Descripción**: Un usuario nuevo se registra en el sistema proporcionando email y contraseña.

**Flujo**:
1. Usuario envía datos de registro
2. Sistema valida formato de email
3. Sistema encripta la contraseña
4. Sistema crea el usuario en la base de datos
5. Sistema retorna confirmación

**Código de Estado**: 201 (Created)

### Caso de Uso 2: Inicio de Sesión

**Descripción**: Un usuario registrado inicia sesión con sus credenciales.

**Flujo**:
1. Usuario envía credenciales
2. Sistema busca usuario por email
3. Sistema verifica contraseña encriptada
4. Sistema genera token JWT
5. Sistema retorna token de acceso

**Código de Estado**: 200 (OK)

### Caso de Uso 3: Acceso a Perfil Protegido

**Descripción**: Un usuario autenticado accede a su perfil personal.

**Flujo**:
1. Usuario envía token JWT en headers
2. Middleware valida token
3. Sistema extrae información del usuario
4. Sistema retorna datos del perfil

**Código de Estado**: 200 (OK)

---

## 📋 Documentación de Prompts

### Prompt de Entrada - Registro de Usuario

**Endpoint**: `POST /api/auth/register`

**Headers**:
```
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Validaciones**:
- Email debe tener formato válido
- Password no puede estar vacío
- Email debe ser único en la base de datos

### Prompt de Salida - Registro de Usuario

**Respuesta Exitosa (201)**:
```json
{
  "message": "User created",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "password": "$2b$10$hashedPassword...",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T00:00:00.000Z"
  }
}
```

**Respuesta de Error (400/409)**:
```json
{
  "error": "Email already exists"
}
```

---

### Prompt de Entrada - Inicio de Sesión

**Endpoint**: `POST /api/auth/login`

**Headers**:
```
Content-Type: application/json
```

**Body (JSON)**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

### Prompt de Salida - Inicio de Sesión

**Respuesta Exitosa (200)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Respuesta de Error (401)**:
```json
{
  "error": "Invalid credentials"
}
```

---

### Prompt de Entrada - Acceso a Perfil

**Endpoint**: `GET /api/auth/profile`

**Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Prompt de Salida - Acceso a Perfil

**Respuesta Exitosa (200)**:
```json
{
  "message": "Perfil accedido correctamente",
  "user": {
    "id": 1
  }
}
```

**Respuesta de Error (401/403)**:
```json
{
  "error": "Token required"
}
```

---

## 🔒 Seguridad

### Medidas Implementadas

1. **Encriptación de Contraseñas**: Uso de bcrypt con salt rounds de 10
2. **Tokens JWT**: Autenticación stateless con expiración de 1 hora
3. **Validación de Email**: Verificación de formato de email
4. **Middleware de Autenticación**: Protección de rutas sensibles
5. **Variables de Entorno**: Configuración segura de base de datos

### Recomendaciones de Seguridad

1. **Cambiar Secret Key**: Reemplazar "secretkey" por una clave secreta fuerte
2. **Rate Limiting**: Implementar límites de intentos de login
3. **HTTPS**: Usar conexiones seguras en producción
4. **Validación de Entrada**: Agregar validaciones más robustas
5. **Logging**: Implementar logs de seguridad

---

## 🛠️ Troubleshooting

### Errores Comunes

#### Error de Conexión a Base de Datos
```
Error al conectar la base de datos: [error details]
```

**Solución**:
1. Verificar variables de entorno en `.env`
2. Confirmar que PostgreSQL esté ejecutándose
3. Verificar credenciales de base de datos

#### Error de Token Inválido
```json
{
  "error": "Invalid token"
}
```

**Solución**:
1. Verificar que el token no haya expirado
2. Confirmar formato correcto: `Bearer [token]`
3. Regenerar token mediante nuevo login

#### Error de Credenciales Inválidas
```json
{
  "error": "Invalid credentials"
}
```

**Solución**:
1. Verificar email y contraseña
2. Confirmar que el usuario existe
3. Verificar que la contraseña sea correcta

### Logs del Sistema

**Inicio Exitoso**:
```
Servidor en puerto 4000
Conectado a la base de datos.
```

**Error de Base de Datos**:
```
Error al conectar la base de datos: [error details]
```

---

## 📚 Referencias

- [Express.js Documentation](https://expressjs.com/)
- [Sequelize Documentation](https://sequelize.org/)
- [JWT.io](https://jwt.io/)
- [bcrypt Documentation](https://github.com/dcodeIO/bcrypt.js)

---

## Soporte

Para soporte técnico o preguntas sobre este sistema de autenticación, contactar al equipo de desarrollo de Vibe Coding.

**Versión**: 1.0.0  
**Última Actualización**: Enero 2024  
**Autor**: Vibe Coding Team 