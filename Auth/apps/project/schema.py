from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from apps.account.models import *


class PojectCreate(BaseModel):
    name: str
    short_name: str
    start_date: str
    end_date: str
    is_active: Boolean
    recipient: Optional[List[str]] = []
    manage_by: int


class ProjectCreate(PojectCreate):
    pass

class ProjectUpdate(PojectCreate):
    pass

class ProjectInDB(PojectCreate):
    id: int

class ProjectOut(ProjectInDB):
    pass

class CustomBooleanField(BaseModel):
    # Custom Pydantic model for handling SQLAlchemy Boolean type
    value: bool

# Use CustomBooleanField in the ProjectBase model
class ProjectBaseWithCustomBoolean(PojectCreate):
    is_active: CustomBooleanField


class Workflowstages(BaseModel):
    name :str
    project : int 


class Role(BaseModel):
    name :str
    can_create_task : Boolean


class ProjectDeveloper(BaseModel):
    project : int
    created : datetime
    is_active : Boolean
    developer : int
    role : int


class Sprint(BaseModel):
    name :str
    description :str
    start_date : datetime
    end_date : datetime


class Task(BaseModel):
    title :str
    created_at : datetime
    resolved_at : datetime
    estimate_time : Boolean
    is_deleted : datetime
    assignee : int
    project : int
    sprint : int
    status : int
    created : int
    deleted_by : int


class TaskPlanner(BaseModel):
    title : str
    priority : int
    status : int
    created : datetime
    user : int