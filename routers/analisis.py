from fastapi import APIRouter, HTTPException
from models import Presupuesto, MetaAhorro
import data
from datetime import date

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

@router.post("/meta")
def evaluar_meta(meta: MetaAhorro):
    gastos = data.obtener_gastos()
    mes_actual = date.today().month
    anio_actual = date.today().year

    gastos_del_mes = [
        g for g in gastos.values()
        if g.fecha.month == mes_actual and g.fecha.year == anio_actual
    ]

    total_mes = sum(g.monto for g in gastos_del_mes)
    disponible = meta.limite_mensual - total_mes
    porcentaje = (total_mes / meta.limite_mensual) * 100 if meta.limite_mensual > 0 else 0

    if porcentaje <= 50:
        estado = "excelente"
        mensaje = "Vas muy bien, sigues dentro de tu meta"
    elif porcentaje <= 75:
        estado = "bien"
        mensaje = "Vas bien pero empieza a controlar los gastos"
    elif porcentaje <= 100:
        estado = "precaucion"
        mensaje = "Estás cerca del límite, ten cuidado"
    else:
        estado = "superado"
        mensaje = "Superaste tu meta de gasto mensual"

    return {
        "mes": mes_actual,
        "anio": anio_actual,
        "limite_mensual": meta.limite_mensual,
        "total_gastado_mes": total_mes,
        "disponible": disponible,
        "porcentaje_usado": round(porcentaje, 2),
        "cantidad_gastos_mes": len(gastos_del_mes),
        "estado": estado,
        "mensaje": mensaje
    }