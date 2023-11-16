from apps.project.models import *
from config.settings import *
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from apps.project.schema import *
from fastapi.encoders import jsonable_encoder
from typing import List
from apps.project.models import Project


Base.metadata.create_all(bind=engine)
project_router = APIRouter()

#created the project
@project_router.post("/projects", response_model=ProjectResponse)
async def create_project(project: PojectCreate, session: Session = Depends(get_session)):
    start_date = datetime.strptime(project.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(project.end_date, '%Y-%m-%d')


    db_project = Project(
        name=project.name,
        short_name=project.short_name,
        start_date=start_date,
        end_date=end_date,
        is_active=project.is_active,
        manage_by=project.manage_by
    )

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    # Include the required fields in the response
    response = ProjectResponse(
        id=db_project.id,
        name=db_project.name,
        short_name=db_project.short_name,
        start_date=db_project.start_date,
        end_date=db_project.end_date,
        is_active=db_project.is_active,
        manage_by=db_project.manage_by
    )
    return response

#update the project
@project_router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project: PojectCreate,
    session: Session = Depends(get_session)
):
    # Query the project by its ID
    db_project = session.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update the project properties
    db_project.name = project.name
    db_project.short_name = project.short_name
    db_project.start_date = datetime.strptime(project.start_date, '%Y-%m-%d')
    db_project.end_date = datetime.strptime(project.end_date, '%Y-%m-%d')
    db_project.is_active = project.is_active
    db_project.manage_by = project.manage_by

    session.commit()
    session.refresh(db_project)

    return ProjectResponse(
        id=db_project.id,
        name=db_project.name,
        short_name=db_project.short_name,
        start_date=db_project.start_date,
        end_date=db_project.end_date,
        is_active=db_project.is_active,
        manage_by=db_project.manage_by
    )

#list of the project
@project_router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(session: Session = Depends(get_session)):
    projects = session.query(Project).all()
    return jsonable_encoder(projects)

#delete the project
@project_router.delete("/projects/{project_id}", response_model=MessageResponse)
async def delete_project(project_id: int, session: Session = Depends(get_session)):
    # Query the project by its ID
    db_project = session.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Delete the project from the database
    session.delete(db_project)
    session.commit()
    return MessageResponse(message="Project successfully deleted")



#workflow created
@project_router.post("/workflowstages", response_model=WorkflowStageResponse)
async def create_workflow_stage(stage: CreateWorkflowstages, session: Session = Depends(get_session)):
    db_stage = WorkFlowStages(**stage.dict())
    session.add(db_stage)
    session.commit()
    session.refresh(db_stage)
    return db_stage


# workflow_stages list
@project_router.get("/workflowstages", response_model=List[WorkflowStageResponse])
async def list_workflow_stages(session: Session = Depends(get_session)):
    stages = session.query(WorkFlowStages).all()
    return jsonable_encoder(stages)

# Get a specific workflow stage by ID
@project_router.get("/workflowstages/{stage_id}", response_model=WorkflowStageResponse)
async def get_workflow_stage(stage_id: int, session: Session = Depends(get_session)):
    stage = session.query(WorkFlowStages).filter(WorkFlowStages.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Workflow stage not found")
    return stage

# Update workflow_stage
@project_router.put("/workflowstages/{stage_id}", response_model=WorkflowStageResponse)
async def update_workflow_stage(stage_id: int, stage: CreateWorkflowstages, session: Session = Depends(get_session)):
    db_stage = session.query(WorkFlowStages).filter(WorkFlowStages.id == stage_id).first()
    if not db_stage:
        raise HTTPException(status_code=404, detail="Workflow stage not found")
    
    for field, value in stage.dict().items():
        setattr(db_stage, field, value)

    session.commit()
    session.refresh(db_stage)
    return db_stage


# Delete a workflow stage
# @project_router.delete("/workflowstages/{stage_id}", response_model=MessageResponse)
# async def delete_workflow_stage(stage_id: int, session: Session = Depends(get_session)):
#     db_stage = session.query(WorkFlowStages).filter(WorkFlowStages.id == stage_id).first()
#     if not db_stage:
#         raise HTTPException(status_code=404, detail="Workflow stage not found")
    
#     session.delete(db_stage)
#     session.commit()
    
#     return MessageResponse(message="Workflow stage successfully deleted")

#sprint_created 
@project_router.post("/sprints", response_model=SprintResponse)
async def create_sprint(sprint: SprintCreate, session: Session = Depends(get_session)):
    db_sprint = Sprint(**sprint.dict())
    session.add(db_sprint)
    session.commit()
    session.refresh(db_sprint)
    return db_sprint


@project_router.get("/sprints", response_model=List[SprintResponse])
async def list_sprints(session: Session = Depends(get_session)):
    sprints = session.query(Sprint).all()
    return jsonable_encoder(sprints)

# Get a specific sprint by ID
@project_router.get("/sprints/{sprint_id}", response_model=SprintResponse)
async def get_sprint(sprint_id: int, session: Session = Depends(get_session)):
    sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

# Update a sprint
@project_router.put("/sprints/{sprint_id}", response_model=SprintResponse)
async def update_sprint(sprint_id: int, sprint: SprintCreate, session: Session = Depends(get_session)):
    db_sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not db_sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    for field, value in sprint.dict().items():
        setattr(db_sprint, field, value)

    session.commit()
    session.refresh(db_sprint)
    
    return db_sprint

# Delete a sprint
@project_router.delete("/sprints/{sprint_id}", response_model=MessageResponse)
async def delete_sprint(sprint_id: int, session: Session = Depends(get_session)):
    db_sprint = session.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not db_sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    session.delete(db_sprint)
    session.commit()
    return MessageResponse(message="Sprint successfully deleted")

#role assign
@project_router.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleCreate, session: Session = Depends(get_session)):
    db_role = Role(**role.dict())
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

@project_router.get("/roles", response_model=RoleListResponse)
async def list_roles(session: Session = Depends(get_session)):
    roles = session.query(Role).all()
    return {"items": roles}

#project developer api
@project_router.post("/projectdevelopers", response_model=ProjectDeveloperResponse)
async def create_project_developer(developer: ProjectDeveloperCreate, session: Session = Depends(get_session)):
    try:
        # Validate that the provided role_id exists in the roles table
        role_exists = session.query(Role).filter(Role.id == developer.role).first()
        if not role_exists:
            raise HTTPException(status_code=400, detail="Invalid role_id")

        db_project_developer = ProjectDeveloper(**developer.dict())
        session.add(db_project_developer)
        session.commit()
        session.refresh(db_project_developer)
        return db_project_developer
    finally:
        session.close()

@project_router.get("/projectdevelopers", response_model=ProjectDeveloperListResponse)
async def list_project_developers(session: Session = Depends(get_session)):
    project_developers = session.query(ProjectDeveloper).all()
    return {"items": project_developers}


#created task api
@project_router.post("/tasks", response_model=TaskResponse)
async def create_task(task_create: TaskCreate, session: Session = Depends(get_session)):
    try:
        db_task = Tasks(**task_create.dict())
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    except Exception as e:
        print(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
#update the task
@project_router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    
    db_task = session.query(Tasks).filter(Tasks.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found") 
    
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    
    if task_update.workflowstage_id:
        workflow_stage = session.query(WorkFlowStages).get(task_update.workflowstage_id)
        if not workflow_stage:
            raise HTTPException(status_code=404, detail="Workflow stage not found")
        db_task.workflowstage = workflow_stage
    session.commit()
    session.refresh(db_task)
    return db_task

#delete the task
@project_router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    db_task = session.query(Tasks).filter(Tasks.id == task_id).first()#Fetch the task from the database

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.is_deleted = True
    db_task.deleted_at = datetime.utcnow()

    session.commit()
    return {"message": "Task deleted successfully"}
