import httpx
from datetime import datetime, timedelta
from app.utils.cache import cache
from app.config import settings

class ClickUpService:
    @cache(ttl=3600)  # Cache de 1 hora
    async def get_team_tasks(self, team_id: str, token: str):
        """Fetch tasks with caching and error handling"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.CLICKUP_API_URL}/team/{team_id}/task",
                    headers={"Authorization": token},
                    params={
                        "include_closed": True,
                        "subtasks": True,
                        "date_updated_gt": int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
                    }
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            # Log error and re-raise
            raise