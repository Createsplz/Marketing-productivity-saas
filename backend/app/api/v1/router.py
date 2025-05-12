from fastapi import APIRouter
from app.api.v1.endpoints import auth, clickup, reports, scoring

api_router = APIRouter()

# Inclui as rotas de autenticação
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Inclui as rotas do ClickUp
api_router.include_router(clickup.router, tags=["ClickUp"])

# Inclui as rotas de relatórios
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Inclui as rotas de pontuação
api_router.include_router(scoring.router, prefix="/scoring", tags=["Scoring"])
