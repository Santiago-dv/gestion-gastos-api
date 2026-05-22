from models import Gasto

gastos_db = {}
contador_id = 1

def agregar_gasto(gasto: Gasto):
    global contador_id
    gastos_db[contador_id] = gasto
    contador_id += 1
    return contador_id - 1

def obtener_gastos():
    return gastos_db

def obtener_gasto(id: int):
    return gastos_db.get(id)

def actualizar_gasto(id: int, datos):
    if id not in gastos_db:
        return None
    gasto_actual = gastos_db[id]
    datos_actualizados = datos.dict(exclude_unset=True)
    gasto_actualizado = gasto_actual.copy(update=datos_actualizados)
    gastos_db[id] = gasto_actualizado
    return gasto_actualizado

def eliminar_gasto(id: int):
    if id not in gastos_db:
        return False
    del gastos_db[id]
    return True