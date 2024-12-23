
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from bot import send_order
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
origins = [
    "https://tu_dominio.com",  # Reemplaza con tu dominio
    "http://localhost:3000",    # Si estás desarrollando localmente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Definir el modelo de datos para el pedido
class Bouquet(BaseModel):
    name: str
    price: float
    image_path: str = None  # Ruta local de la imagen

class Order(BaseModel):
    bouquets: list[Bouquet]
    total: float
    delivery_date: str
    delivery_time: str
    delivery_address: str
    comments: str = None

@app.post("/new_order")
async def new_order(order: Order):
    try:
        await send_order(order.dict())
        return {"status": "success", "message": "Pedido enviado a Telegram"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
