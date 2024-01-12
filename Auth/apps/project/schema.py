from pydantic import BaseModel, EmailStr
from typing import List
from datetime import date
from apps.account.schema import *


class ProjectBase(BaseModel):
    name: str
    short_name: str
    start_date: date
    end_date: date
    is_active: bool
    manage_by: int

class ProjectCreate(ProjectBase):
    pass

class ProjectResponseList(BaseModel):
    id: int
    name: str
    short_name: str
    start_date: date
    end_date: date
    is_active:  bool
    
    manage_by: UserResponse

class ProjectUpdate(BaseModel):
    
    name: str
    short_name: str
    start_date: date
    end_date: date
    is_active: bool
    manage_by: int


class ProjectResponse(BaseModel):
    id: int
    users: List[UserResponse]
    developer: List["ProjectDeveloperResponse"]
    workflowstages: List["WorkFlowStagesResponse"]
    projectdevelopers: List["ProjectDeveloperResponse"]
    task: List["TaskResponse"]


    # class Config:
    #     # Change 'orm_mode' to 'from_attributes'
    #     from_attributes = True
    class Config:
        orm_mode = True
        

class MessageResponse(BaseModel):
    message: str

class WorkFlowStagesBase(BaseModel):
    name: str
    project_id: int


class WorkFlowStagesCreate(WorkFlowStagesBase):
    pass

class WorkFlowStagesResponse(BaseModel):
    id: int
    name: str
    project_id: int

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str
    can_create_task: bool

class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True

class ProjectDeveloperBase(BaseModel):
    project_id: int
    developer: int
    role_id: int

class ProjectDeveloperCreate(ProjectDeveloperBase):
    pass

class ProjectDeveloperResponse(BaseModel):
    id: int
    created: datetime
    is_active: bool
    project: ProjectResponse
    projects: List[ProjectResponse]
    users: UserResponse
    roles: RoleResponse

    class Config:
        orm_mode = True

class SprintBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime

class SprintCreate(SprintBase):
    pass

class SprintResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    task_title: str
    created_at: datetime
    resolved_at: datetime
    estimate_time: str
    is_deleted: bool
    deleted_at: datetime
    created_id: int
    assignee_id: int
    project_id: int
    stage_id: int
    deletedby_id: int
    sprint_id: int

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    users: List[UserResponse]
    projects: List[ProjectResponse]
    workflowstages: List[WorkFlowStagesResponse]
    sprints: List[SprintResponse]

    class Config:
        orm_mode = True

class TaskPlannerBase(BaseModel):
    title: str
    priority: int
    status: str
    user_id: int

class TaskPlannerCreate(TaskPlannerBase):
    pass

class TaskPlannerResponse(BaseModel):
    id: int
    user: UserResponse

    class Config:
        orm_mode = True
