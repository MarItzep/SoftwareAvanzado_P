

from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app import models

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

def seed_data(db: Session):
    servidor = models.ConfigurationItem(
        nombre="Servidor1",
        tipo="Hardware",
        estado_actual="Activo",
        ambiente="PROD"
    )
    app = models.ConfigurationItem(
        nombre="Aplicación1",
        tipo="Software",
        estado_actual="Activo",
        ambiente="PROD"
    )
    db.add(servidor)
    db.add(app)
    db.commit()

    relation = models.Relation(
        ci_padre_id=servidor.id,
        ci_hijo_id=app.id,
        tipo_relacion="depende_de"
    )
    db.add(relation)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()
    print(" Datos de ejemplo insertados correctamente")
