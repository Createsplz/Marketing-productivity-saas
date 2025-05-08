from fastapi import APIRouter

router = APIRouter()

@router.get("/pdf")
async def generate_pdf():
    return {"message": "PDF gerado com sucesso"}
