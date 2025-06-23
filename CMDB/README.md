# Guía de Configuración del Proyecto

## Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Configuración de Base de Datos

### Credenciales por defecto:
- **Usuario:** `postgres`
- **Contraseña:** `admin`
- **URL de conexión:** `postgresql://postgres:admin@localhost:5432/cmdb_db`

### Variable de entorno:
```bash
export DATABASE_URL="postgresql://postgres:admin@localhost:5432/cmdb_db"
```

## Preparación de la Base de Datos

### Crear base de datos (si no existe):
```bash
createdb cmdb_db
```

### Cargar datos de ejemplo:
```bash
python scripts/data.py
```

## Ejecutar el Servidor

```bash
uvicorn app.main:app --reload
```

## Ejecutar Tests Unitarios

```bash
pytest
```

---

### Notas Adicionales

- Asegúrate de tener PostgreSQL instalado y ejecutándose
- El servidor se ejecutará por defecto en `http://localhost:8000`
- El flag `--reload` permite recarga automática durante el desarrollo