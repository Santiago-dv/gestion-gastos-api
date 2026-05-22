from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class Gasto(BaseModel):
    descripcion: str
    monto: float
    categoria: str
    fecha: date

    @field_validator("monto")
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v

    @field_validator("descripcion")
    def descripcion_no_vacia(cls, v):
        if not v.strip():
            raise ValueError("La descripción no puede estar vacía")
        return v.strip()

    @field_validator("categoria")
    def categoria_valida(cls, v):
        categorias = ["comida", "transporte", "ocio", "salud", "educacion", "otros"]
        if v.lower() not in categorias:
            raise ValueError(f"Categoría inválida. Las válidas son: {categorias}")
        return v.lower()

    @field_validator("fecha")
    def fecha_no_futura(cls, v):
        if v > date.today():
            raise ValueError("La fecha no puede ser futura")
        return v

class GastoActualizar(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    categoria: Optional[str] = None
    fecha: Optional[date] = None

    @field_validator("monto")
    def monto_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v

    @field_validator("categoria")
    def categoria_valida(cls, v):
        if v is not None:
            categorias = ["comida", "transporte", "ocio", "salud", "educacion", "otros"]
            if v.lower() not in categorias:
                raise ValueError(f"Categoría inválida. Las válidas son: {categorias}")
            return v.lower()
        return v

class Presupuesto(BaseModel):
    categoria: str
    limite: float

    @field_validator("limite")
    def limite_positivo(cls, v):
        if v <= 0:
            raise ValueError("El límite debe ser mayor a 0")
        return v