from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.clickup import Team, Member, Task
from app.database.models.scoring import ScoringRule
from datetime import datetime


# ⬇️ 1. Cálculo do score de cada tarefa
async def calculate_score(db: AsyncSession, task_data: dict) -> int:
    score = 0
    result = await db.execute(select(ScoringRule))
    rules = result.scalars().all()

    for rule in rules:
        if rule.name.lower() == "concluída" and task_data.get("status", {}).get("status") == "closed":
            score += rule.points
        if rule.name.lower() == "urgente" and task_data.get("priority") == "urgent":
            score += rule.points
        # Adicione mais regras conforme necessário

    return score


# ⬇️ 2. Salvar equipe e membros (sem deletar)
async def save_team_and_members(db: AsyncSession, team_data: dict):
    team_id = str(team_data["id"])

    result = await db.execute(select(Team).where(Team.id == team_id))
    existing_team = result.scalars().first()

    if existing_team:
        existing_team.name = team_data["name"]
        existing_team.color = team_data.get("color")
        existing_team.avatar = team_data.get("avatar")
        team = existing_team
    else:
        team = Team(
            id=team_id,
            name=team_data["name"],
            color=team_data.get("color"),
            avatar=team_data.get("avatar")
        )
        db.add(team)

    await db.flush()

    for m in team_data.get("members", []):
        member_id = str(m["user"]["id"])
        existing_member = await db.get(Member, member_id)

        if existing_member:
            existing_member.username = m["user"]["username"]
            existing_member.email = m["user"].get("email")
            existing_member.role = m["user"].get("role")
            existing_member.role_key = m["user"].get("role_key")
            existing_member.initials = m["user"].get("initials")
            existing_member.avatar = m["user"].get("profilePicture")
            existing_member.team_id = team_id
        else:
            member = Member(
                id=member_id,
                username=m["user"]["username"],
                email=m["user"].get("email"),
                role=m["user"].get("role"),
                role_key=m["user"].get("role_key"),
                initials=m["user"].get("initials"),
                avatar=m["user"].get("profilePicture"),
                team_id=team_id
            )
            db.add(member)

    await db.commit()


# ⬇️ 3. Salvar tarefas com score e mês coletado (sem deletar)
async def save_clickup_tasks(db: AsyncSession, tasks: list, team_id: str):
    current_month = datetime.utcnow().strftime("%Y-%m")

    print(f"\n➡️ Começando salvamento de tarefas para o time {team_id}")
    print(f"📦 Total de tarefas recebidas do ClickUp: {len(tasks)}")

    for task_data in tasks:
        print(f"📅 Criada em: {task_data.get('date_created')}, Status: {task_data.get('status', {}).get('status')}")  # ✅ tem que estar dentro do for

        assignee_id = None
        if task_data.get("assignees"):
            assignee_id = str(task_data["assignees"][0]["id"])

        score = await calculate_score(db, task_data)
        task_id = task_data["id"]

        existing_task = await db.get(Task, task_id)

        if existing_task:
            existing_task.name = task_data["name"]
            existing_task.status = task_data.get("status", {}).get("status")
            existing_task.date_created = int(task_data.get("date_created")) if task_data.get("date_created") else None
            existing_task.date_updated = int(task_data.get("date_updated")) if task_data.get("date_updated") else None
            existing_task.due_date = int(task_data.get("due_date")) if task_data.get("due_date") else None
            existing_task.assignee_id = assignee_id
            existing_task.team_id = team_id
            existing_task.score = score
        else:
            task = Task(
                id=task_id,
                name=task_data["name"],
                status=task_data.get("status", {}).get("status"),
                date_created=int(task_data.get("date_created")) if task_data.get("date_created") else None,
                date_updated=int(task_data.get("date_updated")) if task_data.get("date_updated") else None,
                due_date=int(task_data.get("due_date")) if task_data.get("due_date") else None,
                assignee_id=assignee_id,
                team_id=team_id,
                score=score,
                month_collected=current_month
            )
            db.add(task)

    await db.commit()
    print(f"✅ Finalizado salvamento de tarefas para o mês {current_month}")
