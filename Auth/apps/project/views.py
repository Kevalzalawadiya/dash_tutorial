from apps.project.models import *
from config.settings import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.project.schema import *




Base.metadata.create_all(bind=engine)

router = APIRouter()





#create project


@router.post("/create_project")
async def create_project(project:PojectCreate, session : Session = Depends(get_session)):
    project = Project(project.name,project.short_name,project.start_date,project.end_date,project.is_active,project.recipient,project.manage_by)
    session.add(project)
    session.commit()
    session.refresh(project)
    return {"message" : "Project created successfully", "project" : project}






