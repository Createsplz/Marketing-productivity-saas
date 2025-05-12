from fastapi import APIRouter, status

router = APIRouter()

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user():
    # Aqui futuramente vamos usar a autenticação
    return {"message": "Usuário autenticado com sucesso"}

