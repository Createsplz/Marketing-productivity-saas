from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional, List

from app.database.session import get_async_session
from app.database.models.scoring import ScoringRule

router = APIRouter()

# Pydantic schema para criação/atualização
class ScoringRuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    points: int

# ➕ Criar nova regra
@router.post("/", response_model=ScoringRuleCreate)
async def create_rule(rule: ScoringRuleCreate, db: AsyncSession = Depends(get_async_session)):
    db_rule = ScoringRule(**rule.dict())
    db.add(db_rule)
    await db.commit()
    await db.refresh(db_rule)
    return db_rule

# 📋 Listar todas as regras
@router.get("/", response_model=List[ScoringRuleCreate])
async def get_rules(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ScoringRule))
    return result.scalars().all()

# ✏️ Atualizar regra existente
@router.put("/{rule_id}", response_model=ScoringRuleCreate)
async def update_rule(rule_id: int, update: ScoringRuleCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(ScoringRule).where(ScoringRule.id == rule_id))
    rule = result.scalar_one_or_none()

    if not rule:
        raise HTTPException(status_code=404, detail="Regra não encontrada")

    for key, value in update.dict().items():
        setattr(rule, key, value)

    await db.commit()
    await db.refresh(rule)
    return rule
