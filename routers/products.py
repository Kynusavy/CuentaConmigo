from fastapi import APIRouter

router = APIRouter(prefix="/products",
                    tags=["products"],
                    responses={404:{"mesagge": "No encontrado"}})

products_list = ["Producto1", "Producto2", "Producto3","Producto4", "Producto5"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]