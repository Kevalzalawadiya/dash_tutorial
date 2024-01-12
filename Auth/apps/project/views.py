from sqlalchemy import exists
from psycopg2 import IntegrityError
from apps.project.models import *
from config.settings import *
from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from apps.project.schema import *
from apps.account.schema import *
from fastapi.encoders import jsonable_encoder
from typing import List
import pytz
from apps.account.models import *
from apps.project.models import Project
from sqlalchemy.exc import DataError
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)
project_router = APIRouter()

#user list
@project_router.get("/user_list", response_model=List[UserResponse])
async def get_user_list(session: Session = Depends(get_session)):
    users = session.query(User).all()
    user_responses = [UserResponse(id=user.id, username=user.username, email=user.email) for user in users]

    return user_responses

#create project
@project_router.post("/create_projects", response_model=ProjectCreate)
async def create_project(project: ProjectCreate, session: Session = Depends(get_session)):

    if not project.start_date or not project.end_date:
        raise HTTPException(status_code=400, detail="Start date and end date are required.")
    
    start_date_str = project.start_date.strftime('%Y-%m-%d')
    end_date_str = project.end_date.strftime('%Y-%m-%d')
 
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")

    user_id = project.manage_by

    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    db_project = Project(
        name=project.name,
        short_name=project.short_name,
        start_date=start_date,
        end_date=end_date,
        is_active=project.is_active,
    
        manage_by=user_id 
    )

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    response = ProjectCreate(
        id=db_project.id,
        name=db_project.name,
        short_name=db_project.short_name,
        start_date=db_project.start_date,
        end_date=db_project.end_date,
        is_active=db_project.is_active,
        manage_by=db_project.manage_by
    )
    return response

@project_router.get("/list_projects", response_model=List[ProjectResponseList])
async def list_projects(session: Session = Depends(get_session)):
    projects = session.query(Project).all()
    project_responses = []

    for project in projects:
        manage_by_user = session.query(User).filter(User.id == project.manage_by).first()

        if manage_by_user:
            manage_by = {
                "id": manage_by_user.id,
                "username": manage_by_user.username,
                "email": manage_by_user.email
            }
        else:
            manage_by = None

        project_response = ProjectResponseList(
            id=project.id,
            name=project.name,
            short_name=project.short_name,
            start_date=project.start_date,
            end_date=project.end_date,
            is_active=project.is_active,
            manage_by=manage_by
        )

        project_responses.append(project_response)

    return project_responses



#list of the project
@project_router.get("/list_projects/{project_id}", response_model=List[ProjectResponseList])
async def list_projects(project_id: int, session: Session = Depends(get_session)):
    projects = session.query(Project).filter(Project.id == project_id).all()
    project_responses = []

    for project in projects:
        manage_by_user = session.query(User).filter(User.id == project.manage_by).first()

        if manage_by_user:
            manage_by = {
                "id": manage_by_user.id,
                "username": manage_by_user.username,
                "email": manage_by_user.email
            }
        else:
            manage_by = None

        project_response = ProjectResponseList(
            id=project.id,
            name=project.name,
            short_name=project.short_name,
            start_date=project.start_date,
            end_date=project.end_date,
            is_active=project.is_active,
            manage_by=manage_by
        )

        project_responses.append(project_response)

    return project_responses


@project_router.put("/update_project/{project_id}", response_model=ProjectUpdate)
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    session: Session = Depends(get_session)
):
    # Check if the project exists
    db_project = session.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the user exists before updating
    db_user = session.query(User).filter(User.id == project.manage_by).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid user ID in manage_by")

    # Update the project details
    db_project.name = project.name
    db_project.short_name = project.short_name
    db_project.start_date = project.start_date
    db_project.end_date = project.end_date
    db_project.is_active = project.is_active

    # Check if the provided manage_by value exists in the User table
    if not session.query(exists().where(User.id == project.manage_by)).scalar():
        raise HTTPException(status_code=400, detail="Invalid user ID in manage_by")

    db_project.manage_by = project.manage_by

    # Handle foreign key constraint violation
    try:
        # Commit the changes
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Foreign key constraint violation: {e}")

    # Return the updated project details in the response
    return project




#delete the project
@project_router.delete("/delete_projects/{project_id}", response_model=MessageResponse)
async def delete_project(project_id: int, session: Session = Depends(get_session)):
    # Query the project by its ID
    db_project = session.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete the project from the database
    session.delete(db_project)
    session.commit()
    return MessageResponse(message="Project successfully deleted")


@project_router.get("/search_projects")
async def search_projects(
    project_name: str = Query(..., title="Project Name"),
    session: Session = Depends(get_session)
):
    projects = (
        session.query(Project)
        .filter(Project.name.ilike(f"%{project_name}%"))
        .all()
    )

    if not projects:
        raise HTTPException(status_code=404, detail=f"No projects found with the specified name: {project_name}")

    result = [
        {
            "id": project.id,
            "name": project.name,
            "short_name": project.short_name,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "is_active": project.is_active,
            "manage_by": project.manage_by,
        }
        for project in projects
    ]

    return result   



# #workflow created
# @project_router.post("/workflowstages", response_model=WorkflowStageResponse)
# async def create_workflow_stage(stage: CreateWorkflowstages, session: Session = Depends(get_session)):
#     db_stage = WorkFlowStages(**stage.dict())
#     session.add(db_stage)
#     session.commit()
#     session.refresh(db_stage)
#     return db_stage


# # workflow_stages list
# @project_router.get("/list_workflowstages", response_model=List[WorkflowStageResponse])
# async def list_workflow_stages(session: Session = Depends(get_session)):
#     stages = session.query(WorkFlowStages).all()
#     return jsonable_encoder(stages)

# # Get a specific workflow stage by ID
# @project_router.get("/id_workflowstages/{stage_id}", response_model=WorkflowStageResponse)
# async def get_workflow_stage(stage_id: int, session: Session = Depends(get_session)):
#     stage = session.query(WorkFlowStages).filter(WorkFlowStages.id == stage_id).first()
#     if not stage:
#         raise HTTPException(status_code=404, detail="Workflow stage not found")
#     return stage

# # Update workflow_stage
# @project_router.put("/update_workflowstages/{stage_id}", response_model=WorkflowStageResponse)
# async def update_workflow_stage(stage_id: int, stage: CreateWorkflowstages, session: Session = Depends(get_session)):
#     db_stage = session.query(WorkFlowStages).filter(WorkFlowStages.id == stage_id).first()
#     if not db_stage:
#         raise HTTPException(status_code=404, detail="Workflow stage not found")
    
#     for field, value in stage.dict().items():
#         setattr(db_stage, field, value)

#     session.commit()
#     session.refresh(db_stage)
#     return db_stage


# # Delete a workflow stage
# @project_router.delete("/delete_workflowstages/{stage_id}", response_model=MessageResponse)
# async def delete_workflow_stage(stage_id: int, session: Session = Depends(get_session)):
#     db_stage = session.query(WorkFlowStages).filter(WorkFlowStages.id == stage_id).first()
#     if not db_stage:
#         raise HTTPException(status_code=404, detail="Workflow stage not found")
    
#     session.delete(db_stage)
#     session.commit()
    
#     return MessageResponse(message="Workflow stage successfully deleted")

# #sprint_created 
# @project_router.post("/create_sprints", response_model=SprintResponse)
# async def create_sprint(sprint: SprintCreate, session: Session = Depends(get_session)):
#     db_sprint = Sprint(**sprint.dict())
#     session.add(db_sprint)
#     session.commit()
#     session.refresh(db_sprint)
#     return db_sprint

# #display sprints
# @project_router.get("/list_sprints", response_model=List[SprintResponse])
# async def list_sprints(session: Session = Depends(get_session)):
#     sprints = session.query(Sprint).all()
#     return jsonable_encoder(sprints)

# # Get a specific sprint by ID
# @project_router.get("/id_sprints/{sprint_id}", response_model=SprintResponse)
# async def get_sprint(sprint_id: int, session: Session = Depends(get_session)):
#     sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
#     if not sprint:
#         raise HTTPException(status_code=404, detail="Sprint not found")
#     return sprint

# # Update a sprint
# @project_router.put("/update_sprints/{sprint_id}", response_model=SprintResponse)
# async def update_sprint(sprint_id: int, sprint: SprintCreate, session: Session = Depends(get_session)):
#     db_sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
#     if not db_sprint:
#         raise HTTPException(status_code=404, detail="Sprint not found")
    
#     for field, value in sprint.dict().items():
#         setattr(db_sprint, field, value)

#     session.commit()
#     session.refresh(db_sprint)
    
#     return db_sprint

# # Delete a sprint
# @project_router.delete("/delete_sprints/{sprint_id}", response_model=MessageResponse)
# async def delete_sprint(sprint_id: int, session: Session = Depends(get_session)):
#     db_sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
#     if not db_sprint:
#         raise HTTPException(status_code=404, detail="Sprint not found")
#     session.delete(db_sprint)
#     session.commit()
#     return MessageResponse(message="Sprint successfully deleted")

# #role assign
# @project_router.post("/roles", response_model=RoleResponse)
# async def create_role(role: RoleCreate, session: Session = Depends(get_session)):
#     db_role = Role(**role.dict())
#     session.add(db_role)
#     session.commit()
#     session.refresh(db_role)
#     return db_role

# #list roles
# @project_router.get("/list_roles", response_model=RoleListResponse)
# async def list_roles(session: Session = Depends(get_session)):
#     roles = session.query(Role).all()
#     return {"items": roles}

# #project developer api
# @project_router.post("/projectdevelopers", response_model=ProjectDeveloperResponse)
# async def create_project_developer(developer: ProjectDeveloperCreate, session: Session = Depends(get_session)):
#     try:
#         # Validate that the provided role_id exists in the roles table
#         role_exists = session.query(Role).filter(Role.id == developer.role).first()
#         if not role_exists:
#             raise HTTPException(status_code=400, detail="Invalid role_id")

#         db_project_developer = ProjectDeveloper(**developer.dict())
#         session.add(db_project_developer)
#         session.commit()
#         session.refresh(db_project_developer)
#         return db_project_developer
#     finally:
#         session.close()

# #list of projectdeveloper
# @project_router.get("/list_projectdevelopers", response_model=ProjectDeveloperListResponse)
# async def list_project_developers(session: Session = Depends(get_session)):
#     project_developers = session.query(ProjectDeveloper).all()
#     return {"items": project_developers}


# #created task api
# @project_router.post("/craete_task", response_model=TaskResponse)
# async def create_task(task_create: TaskCreate, session: Session = Depends(get_session)):
#     try:
#         db_task = Tasks(**task_create.dict())
#         session.add(db_task)
#         session.commit()
#         session.refresh(db_task)
#         return db_task
#     except Exception as e:
#         print(f"Error creating task: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# #update the task
# @project_router.put("/update_tasks/{task_id}", response_model=TaskResponse)
# async def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    
#     db_task = session.query(Tasks).filter(Tasks.id == task_id).first()
#     if not db_task:
#         raise HTTPException(status_code=404, detail="Task not found") 
    
#     for field, value in task_update.dict(exclude_unset=True).items():
#         setattr(db_task, field, value)
    
#     if task_update.workflowstage_id:
#         workflow_stage = session.query(WorkFlowStages).get(task_update.workflowstage_id)
#         if not workflow_stage:
#             raise HTTPException(status_code=404, detail="Workflow stage not found")
#         db_task.workflowstage = workflow_stage
#     session.commit()
#     session.refresh(db_task)
#     return db_task

# #delete the task
# @project_router.delete("/delete_tasks/{task_id}", response_model=dict)
# async def delete_task(task_id: int, session: Session = Depends(get_session)):
#     db_task = session.query(Tasks).filter(Tasks.id == task_id).first()#Fetch the task from the database

#     if not db_task:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     db_task.is_deleted = True
#     db_task.deleted_at = datetime.utcnow()

#     session.commit()
#     return {"message": "Task deleted successfully"}

# #create taskplanner
# @project_router.post("/create_taskplanner/", response_model=TaskPlannerResponse)
# def create_taskplanner(taskplanner_create: TaskPlannerCreate, db: Session = Depends(get_session)):
#     try:
#         db_taskplanner = TaskPlanner(**taskplanner_create.dict())
#         db.add(db_taskplanner)
#         db.commit()
#         db.refresh(db_taskplanner)
#         return db_taskplanner
#     except ValueError as e:
#         print(f"Error creating task planner: {e}")
#     raise HTTPException(status_code=400, detail=str(e))

# #list of taskplanner
# @project_router.get("/list_taskplanner", response_model=List[TaskPlannerResponse])
# def list_taskplanners(db: Session = Depends(get_session)):
#     taskplanners = db.query(TaskPlanner).all()

#     return [
#         TaskPlannerResponse(
#             id=db_taskplanner.id,
#             title=db_taskplanner.title,
#             priority=db_taskplanner.priority,
#             status=db_taskplanner.status,
#             user=db_taskplanner.user,
#             created=db_taskplanner.created 
#         )
#         for db_taskplanner in taskplanners
#     ]

# #update the taskplanner
# @project_router.put("/update_taskplanner/{taskplanner_id}", response_model=TaskPlannerResponse)
# def update_taskplanner(taskplanner_id: int, taskplanner_update: TaskPlannerUpdate, db: Session = Depends(get_session)):
#     db_taskplanner = db.query(TaskPlanner).filter(TaskPlanner.id == taskplanner_id).first()
#     if db_taskplanner is None:
#         raise HTTPException(status_code=404, detail="TaskPlanner not found")

#     for key, value in taskplanner_update.dict().items():
#         setattr(db_taskplanner, key, value)

#     db.commit()
#     db.refresh(db_taskplanner)
#     return db_taskplanner

# #delete the taskplanner
# @project_router.delete("/delete_taskplanner/{taskplanner_id}", response_model=TaskPlannerResponse)
# def delete_taskplanner(taskplanner_id: int, db: Session = Depends(get_session)):
#     db_taskplanner = db.query(TaskPlanner).filter(TaskPlanner.id == taskplanner_id).first()
#     if db_taskplanner is None:
#         raise HTTPException(status_code=404, detail="TaskPlanner not found")

#     db.delete(db_taskplanner)
#     db.commit()
#     print(f"TaskPlanner with ID {taskplanner_id} deleted")
#     return db_taskplanner
