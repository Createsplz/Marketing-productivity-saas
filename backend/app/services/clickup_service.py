import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.repositories.clickup_repository import save_team_and_members, save_clickup_tasks


async def fetch_clickup_teams(db: AsyncSession):
    headers = {
        "Authorization": settings.CLICKUP_API_TOKEN
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.CLICKUP_API_URL}/team", headers=headers)
        response.raise_for_status()
        data = response.json()

        for team in data.get("teams", []):
            await save_team_and_members(db, team)

        return data.get("teams", [])


async def fetch_clickup_tasks(team_id: str, db: AsyncSession):
    headers = {
        "Authorization": settings.CLICKUP_API_TOKEN
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.CLICKUP_API_URL}/team/{team_id}/task",
            headers=headers,
            params={"include_closed": "true"}
        )
        response.raise_for_status()
        data = response.json()

        tasks = data.get("tasks", [])
        print("📥 Total de tarefas recebidas da ClickUp:", len(tasks))  # ✅ ESSENCIAL
        if tasks:
            print("🧪 Primeira tarefa:", tasks[0])  # ✅ AJUDA A VALIDAR ESTRUTURA

        await save_clickup_tasks(db, tasks, team_id)

        return tasks
