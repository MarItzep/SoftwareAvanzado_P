from pydantic import BaseModel
from typing import Optional
from datetime import date
# archivo que define los esquemas de datos para la CMDB
# (Configuration Management Database)
# Este archivo utiliza Pydantic para definir los modelos de datos
# que se utilizaran en la aplicacion
class CIBase(BaseModel):
    nombre: str
    tipo: str
    descripcion: Optional[str] = None
    numero_serie: Optional[str] = None
    version: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    estado_actual: str
    ubicacion_fisica: Optional[str] = None
    propietario: Optional[str] = None
    ambiente: Optional[str] = None
    fecha_cambio: Optional[date] = None
    descripcion_cambio: Optional[str] = None
    enlace_incidente: Optional[str] = None
    enlace_documentacion: Optional[str] = None
    nivel_seguridad: Optional[str] = None
    cumplimiento: Optional[bool] = None
    estado_configuracion: Optional[str] = None
    numero_licencia: Optional[str] = None
    fecha_vencimiento: Optional[date] = None

class CICreate(CIBase):
    pass

class CI(CIBase):
    id: int

    class Config:
        from_attributes = True
