from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import gastos, analisis

app = FastAPI(
    title="API de Gestión de Gastos Personales",
    description="API REST para registrar gastos y analizar salud financiera",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(gastos.router)
app.include_router(analisis.router)

@app.get("/")
def inicio():
    return FileResponse("static/index.html")