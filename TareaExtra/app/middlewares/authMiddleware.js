// authMiddleware.js
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
