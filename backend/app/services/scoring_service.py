from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.scoring import ScoringRule

async def calculate_score(db: AsyncSession, task_data: dict) -> int:
    score = 0
    result = await db.execute(select(ScoringRule))
    rules = result.scalars().all()

    for rule in rules:
        if rule.name.lower() == "concluída" and task_data.get("status", {}).get("status") == "closed":
            score += rule.points
        if rule.name.lower() == "urgente" and task_data.get("priority") == "urgent":
            score += rule.points

    return score
