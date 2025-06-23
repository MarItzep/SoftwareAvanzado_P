from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import database, models, schemas

router = APIRouter(prefix="/relations", tags=["relations"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquemas para las relaciones
class RelationCreate(BaseModel):
    ci_padre_id: int
    ci_hijo_id: int
    tipo_relacion: str

## Esquema para leer las relaciones
class RelationRead(RelationCreate):
    id: int
    class Config:
        from_attributes = True

@router.post("/", response_model=RelationRead)
def create_relation(relation: RelationCreate, db: Session = Depends(get_db)):
    # Verificar que ambos CIs existan
    padre = db.query(models.ConfigurationItem).get(relation.ci_padre_id)
    hijo = db.query(models.ConfigurationItem).get(relation.ci_hijo_id)
    if not padre or not hijo:
        raise HTTPException(status_code=404, detail="CI padre o hijo no encontrado")

    db_relation = models.Relation(
        ci_padre_id=relation.ci_padre_id,
        ci_hijo_id=relation.ci_hijo_id,
        tipo_relacion=relation.tipo_relacion,
    )
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation

@router.get("/padre/{ci_id}", response_model=List[RelationRead])
def list_relations_as_padre(ci_id: int, db: Session = Depends(get_db)):
    relations = db.query(models.Relation).filter(models.Relation.ci_padre_id == ci_id).all()
    return relations

@router.get("/hijo/{ci_id}", response_model=List[RelationRead])
def list_relations_as_hijo(ci_id: int, db: Session = Depends(get_db)):
    relations = db.query(models.Relation).filter(models.Relation.ci_hijo_id == ci_id).all()
    return relations

@router.delete("/{relation_id}", response_model=RelationRead)
def delete_relation(relation_id: int, db: Session = Depends(get_db)):
    relation = db.query(models.Relation).get(relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    db.delete(relation)
    db.commit()
    return relation
