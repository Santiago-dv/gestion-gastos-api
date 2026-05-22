from fastapi import APIRouter, HTTPException
from models import Presupuesto
import data

router = APIRouter(prefix="/analisis", tags=["Análisis"])

@router.post("/")
def analizar_finanzas(presupuestos: list[Presupuesto]):
    gastos = data.obtener_gastos()

    if not gastos:
        raise HTTPException(status_code=404, detail="No hay gastos registrados")

    totales_por_categoria = {}
    for gasto in gastos.values():
        cat = gasto.categoria
        totales_por_categoria[cat] = totales_por_categoria.get(cat, 0) + gasto.monto

    categoria_mayor_gasto = max(totales_por_categoria, key=totales_por_categoria.get)
    total_general = sum(totales_por_categoria.values())

    resultado_por_categoria = {}
    for presupuesto in presupuestos:
        cat = presupuesto.categoria
        gastado = totales_por_categoria.get(cat, 0)
        limite = presupuesto.limite
        porcentaje = (gastado / limite) * 100 if limite > 0 else 0

        if porcentaje <= 75:
            estado = "saludable"
        elif porcentaje <= 100:
            estado = "en riesgo"
        else:
            estado = "déficit"

        resultado_por_categoria[cat] = {
            "gastado": gastado,
            "limite": limite,
            "porcentaje_usado": round(porcentaje, 2),
            "estado": estado
        }

    return {
        "total_general": total_general,
        "categoria_mayor_gasto": categoria_mayor_gasto,
        "analisis_por_categoria": resultado_por_categoria
    }