from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

## Router para la CMDB (Configuration Management Database)
# Este router maneja las operaciones CRUD para los elementos de configuracion
# y sus relaciones, auditorias, etc.

router = APIRouter(prefix="/cis")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CI)
def create_ci(ci: schemas.CICreate, db: Session = Depends(get_db)):
    return crud.create_ci(db, ci)

@router.get("/", response_model=list[schemas.CI])
def list_cis(db: Session = Depends(get_db)):
    return crud.get_cis(db)

@router.get("/{ci_id}", response_model=schemas.CI)
def read_ci(ci_id: int, db: Session = Depends(get_db)):
    db_ci = crud.get_ci(db, ci_id)
    if not db_ci:
        raise HTTPException(status_code=404, detail="CI not found")
    return db_ci

@router.put("/{ci_id}", response_model=schemas.CI)
def update_ci(ci_id: int, ci: schemas.CICreate, db: Session = Depends(get_db)):
    return crud.update_ci(db, ci_id, ci)

@router.delete("/{ci_id}", response_model=schemas.CI)
def delete_ci(ci_id: int, db: Session = Depends(get_db)):
    return crud.delete_ci(db, ci_id)
