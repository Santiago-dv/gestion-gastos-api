from fastapi import APIRouter, HTTPException
from models import Gasto, GastoActualizar
import data

router = APIRouter(prefix="/gastos", tags=["Gastos"])

@router.post("/")
def crear_gasto(gasto: Gasto):
    id = data.agregar_gasto(gasto)
    return {"mensaje": "Gasto creado", "id": id, "gasto": gasto}

@router.get("/")
def listar_gastos():
    gastos = data.obtener_gastos()
    if not gastos:
        return {"mensaje": "No hay gastos registrados"}
    return gastos

@router.get("/{id}")
def obtener_gasto(id: int):
    gasto = data.obtener_gasto(id)
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return gasto

@router.put("/{id}")
def actualizar_gasto(id: int, datos: GastoActualizar):
    gasto = data.actualizar_gasto(id, datos)
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto actualizado", "gasto": gasto}

@router.delete("/{id}")
def eliminar_gasto(id: int):
    eliminado = data.eliminar_gasto(id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto eliminado correctamente"}