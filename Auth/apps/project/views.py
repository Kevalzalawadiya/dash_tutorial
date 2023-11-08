from apps.project.models import *
from config.settings import *
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from apps.project.schema import *
from fastapi.encoders import jsonable_encoder


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
