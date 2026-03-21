from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
 
class AfiliadoResponse(BaseModel):
    id_afiliado:      int
    documento:        str
    nombre:           str
    apellido:         str
    regimen:          str = Field(pattern='^[SC]$')
    estado:           str
    fecha_afiliacion: date
    model_config = {'from_attributes': True}
 
class ElegibilidadResponse(BaseModel):
    afiliado:    AfiliadoResponse
    es_elegible: bool
    mensaje:     str
 
class AutorizacionRequest(BaseModel):
    documento_afiliado: str  = Field(min_length=5, max_length=20)
    codigo_cups:        str  = Field(min_length=5, max_length=10)
    registro_medico:    str
    id_sede:            int  = Field(gt=0)
    codigo_diagnostico: str
 
    @field_validator('codigo_cups')
    @classmethod
    def cups_upper(cls, v: str) -> str:
        return v.upper().strip()
 
class AutorizacionResponse(BaseModel):
    numero_auto: str
    estado:      str
    mensaje:     str
    monto_copago: float
