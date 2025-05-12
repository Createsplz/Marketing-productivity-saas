from fastapi import APIRouter, status

router = APIRouter()

@router.get("/pdf", status_code=status.HTTP_200_OK)
async def generate_pdf():
    # Aqui no futuro vamos gerar e retornar um PDF real
    return {"message": "PDF gerado com sucesso"}
