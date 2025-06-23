from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# configuracion  de la base de datos para la CMDB 
# (Configuration Management Database)
# Esta base de datos almacena los elementos de configuracion, s
# us relaciones y auditorias
class ConfigurationItem(Base):
    __tablename__ = "configuration_items"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tipo = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    numero_serie = Column(String, nullable=True)
    version = Column(String, nullable=True)
    fecha_adquisicion = Column(Date, nullable=True)
    estado_actual = Column(String, index=True)
    ubicacion_fisica = Column(String, nullable=True)
    propietario = Column(String, nullable=True)
    ambiente = Column(String, nullable=True)
    fecha_cambio = Column(Date, nullable=True)
    descripcion_cambio = Column(String, nullable=True)
    enlace_incidente = Column(String, nullable=True)
    enlace_documentacion = Column(String, nullable=True)
    nivel_seguridad = Column(String, nullable=True)
    cumplimiento = Column(Boolean, default=False)
    estado_configuracion = Column(String, nullable=True)
    numero_licencia = Column(String, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)

    hijos = relationship("Relation", back_populates="padre", foreign_keys='Relation.ci_padre_id')
    padres = relationship("Relation", back_populates="hijo", foreign_keys='Relation.ci_hijo_id')
    auditorias = relationship("AuditLog", back_populates="ci")


class Relation(Base):
    __tablename__ = "relations"
    id = Column(Integer, primary_key=True, index=True)
    ci_padre_id = Column(Integer, ForeignKey('configuration_items.id'))
    ci_hijo_id = Column(Integer, ForeignKey('configuration_items.id'))
    tipo_relacion = Column(String)

    padre = relationship("ConfigurationItem", back_populates="hijos", foreign_keys=[ci_padre_id])
    hijo = relationship("ConfigurationItem", back_populates="padres", foreign_keys=[ci_hijo_id])


## AuditLog almacena las auditorias de los
#  cambios realizados en los elementos de configuracion
class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(Integer, primary_key=True, index=True)
    ci_id = Column(Integer, ForeignKey('configuration_items.id'))
    accion = Column(String)
    timestamp = Column(Date)
    usuario = Column(String)

    ci = relationship("ConfigurationItem", back_populates="auditorias")
