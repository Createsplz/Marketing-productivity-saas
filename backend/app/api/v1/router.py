from fastapi import APIRouter
from app.api.v1.endpoints import auth, clickup, reports

api_router = APIRouter()

# Inclui as rotas de autenticação
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Inclui as rotas do ClickUp
api_router.include_router(clickup.router, prefix="/clickup", tags=["ClickUp"])

# Inclui as rotas de relatórios
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
