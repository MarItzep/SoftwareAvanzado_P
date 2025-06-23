from sqlalchemy.orm import Session
from app import models, schemas
## crud de la base de datos para la CMDB
# (Configuration Management Database)
# Este archivo contiene las operaciones CRUD (Create, Read, Update, Delete)
def create_ci(db: Session, ci: schemas.CICreate):
    db_ci = models.ConfigurationItem(**ci.dict())
    db.add(db_ci)
    db.commit()
    db.refresh(db_ci)
    return db_ci

def get_ci(db: Session, ci_id: int):
    return db.query(models.ConfigurationItem).filter(models.ConfigurationItem.id == ci_id).first()

def get_cis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ConfigurationItem).offset(skip).limit(limit).all()

def update_ci(db: Session, ci_id: int, ci: schemas.CICreate):
    db_ci = get_ci(db, ci_id)
    for key, value in ci.dict().items():
        setattr(db_ci, key, value)
    db.commit()
    db.refresh(db_ci)
    return db_ci

def delete_ci(db: Session, ci_id: int):
    db_ci = get_ci(db, ci_id)
    if db_ci:
        db.delete(db_ci)
        db.commit()
    return db_ci
