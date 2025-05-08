from fastapi import APIRouter

router = APIRouter()

@router.get("/sync")
async def sync_clickup_data():
    return {"message": "Dados do ClickUp sincronizados com sucesso"}
