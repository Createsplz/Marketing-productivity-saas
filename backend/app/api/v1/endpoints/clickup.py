from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from datetime import datetime, timedelta
from app.database.session import get_async_session
from app.database.models.clickup import Task, Member
from app.schemas.task import TaskWithScoreResponse
from app.services.clickup_service import fetch_clickup_teams, fetch_clickup_tasks

router = APIRouter()

# 🔄 Sincronizar dados da equipe e membros via API do ClickUp
@router.get("/sync")
async def sync_clickup_data(db: AsyncSession = Depends(get_async_session)):
    try:
        teams = await fetch_clickup_teams(db)
        return {"message": "Sincronizado com sucesso", "teams": teams}
    except Exception as e:
        return {"error": str(e)}

# 📥 Buscar tarefas da API do ClickUp e salvar no banco
@router.get("/tasks/{team_id}", status_code=status.HTTP_200_OK)
async def get_clickup_tasks(team_id: str, db: AsyncSession = Depends(get_async_session)):
    tasks = await fetch_clickup_tasks(team_id, db)
    print("📥 Tarefas recebidas do ClickUp:", len(tasks))
    return tasks

# 📊 Buscar tarefas do banco com score e nome do responsável
@router.get("/tasks-with-score/{team_id}", response_model=list[TaskWithScoreResponse])
async def get_tasks_with_score(
    team_id: str,
    month: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    print(f"🔍 Buscando tarefas do time {team_id} para o mês: {month or 'todos'}")

    query = select(Task, Member.username).join(Member, Task.assignee_id == Member.id, isouter=True).where(Task.team_id == team_id)

    if month and len(month.strip()) == 7:
        query = query.where(Task.month_collected == month.strip())

    result = await db.execute(query)
    results = result.all()

    print(f"📦 Total encontrado: {len(results)}")

    return [
        TaskWithScoreResponse(
            id=task.id,
            name=task.name,
            status=task.status,
            score=task.score,
            assignee_id=task.assignee_id,
            assignee_name=username or "Não atribuído"
        )
        for task, username in results
    ]
@router.get("/tasks-summary/{team_id}")
async def get_tasks_summary(
    team_id: str,
    month: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    if not month:
        return {"error": "O parâmetro 'month' é obrigatório. Ex: 2025-05"}

    try:
        start_date = datetime.strptime(month, "%Y-%m")
        end_month = start_date.replace(day=28) + timedelta(days=4)  # Vai para o próximo mês
        end_date = end_month.replace(day=1)  # Primeiro dia do próximo mês
    except ValueError:
        return {"error": "Formato de 'month' inválido. Use YYYY-MM."}

    # Criadas no mês
    created_query = select(Task).where(
        Task.team_id == team_id,
        Task.date_created >= start_date.timestamp() * 1000,
        Task.date_created < end_date.timestamp() * 1000
    )
    # Concluídas no mês
    closed_query = select(Task).where(
        Task.team_id == team_id,
        Task.status == "closed",
        Task.date_updated >= start_date.timestamp() * 1000,
        Task.date_updated < end_date.timestamp() * 1000
    )
    # Em aberto (ainda não concluídas)
    open_query = select(Task).where(
        Task.team_id == team_id,
        Task.status != "closed"
    )

    created = len((await db.execute(created_query)).scalars().all())
    closed = len((await db.execute(closed_query)).scalars().all())
    open_ = len((await db.execute(open_query)).scalars().all())

    return {
        "month": month,
        "created": created,
        "closed": closed,
        "open": open_
    }

    
@router.get("/debug/tasks-raw")
async def debug_tasks_raw(db: AsyncSession = Depends(get_async_session)):
    tasks = await db.execute(select(Task))
    data = tasks.scalars().all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "date_created": t.date_created,
            "month_collected": t.month_collected
        } for t in data
    ]


