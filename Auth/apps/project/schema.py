from pydantic import BaseModel,validator
from datetime import datetime
from typing import Optional, List
from apps.account.models import *



class PojectCreate(BaseModel):
    name: str
    short_name: str
    start_date: str
    end_date: str
    is_active: bool  # Use 'bool' instead of 'Boolean'
    # recipient: Optional[List[str]] = []
    manage_by: int

    
class ProjectResponse(BaseModel):
    id: int
    name: str
    short_name: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    # recipient: list
    manage_by: int

class ProjectCreate(PojectCreate):
    pass

class ProjectUpdate(PojectCreate):
    pass

class MessageResponse(BaseModel):
    message: str
    
class ProjectInDB(PojectCreate):
    id: int

class ProjectOut(ProjectInDB):
    pass

class CustomBooleanField(BaseModel):
    value: bool

class ProjectBaseWithCustomBoolean(PojectCreate):
    is_active: CustomBooleanField

#workflow
class CreateWorkflowstages(BaseModel):
    name :str
    id : int 

class WorkflowStageResponse(BaseModel):
    id: int
    name: str
    id: int

class WorkflowStageInDB(CreateWorkflowstages):
    id: int

class WorkflowStageOut(WorkflowStageInDB):
    pass

class WorkflowStageListResponse(BaseModel):
    items: List[WorkflowStageResponse]



class RoleBase(BaseModel):
    name :str
    can_create_task : bool

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

class RoleListResponse(BaseModel):
    items: list[RoleResponse]



class ProjectDeveloperBase(BaseModel):
    project : int
    created : datetime
    is_active : bool
    developer : int
    role : int

class ProjectDeveloperCreate(ProjectDeveloperBase):
    pass

class ProjectDeveloperResponse(ProjectDeveloperBase):
    id: int

class ProjectDeveloperListResponse(BaseModel):
    items: list[ProjectDeveloperResponse]

#sprint
class SprintBase(BaseModel):
    name :str
    description :str
    start_date : datetime
    end_date : datetime

class SprintCreate(SprintBase):
    pass

class SprintResponse(SprintBase):
    id: int

class SprintListResponse(BaseModel):
    items: List[SprintResponse]

class TaskCreate(BaseModel):
    task_title: str
    created_at: datetime
    resolved_at: datetime
    is_deleted: bool
    # estimate_time: Optional[str] = '00:00'
    is_deleted: bool
    deleted_at: datetime
    assignee: int
    project_id: int  # Update this line
    sprint: Optional[int] = None
    workflowstage_id: Optional[int] = None

# class TaskResponse(BaseModel):
#     id: int
#     task_title: str
#     created_at: datetime
#     resolved_at: datetime
#     # estimate_time: str
#     is_deleted: bool
#     deleted_at: datetime
#     assignee: int
#     project: int
#     project_id: int 
#     sprint: int
#     workflowstage_id: int
#     created: int
#     deleted_by: int
class TaskResponse(BaseModel):
    id: int
    task_title: str
    created_at: datetime
    resolved_at: datetime
    # estimate_time: str
    is_deleted: bool
    deleted_at: datetime
    assignee: int
    project_id: int 
    sprint: int
    workflowstage_id: int
    created: Optional[int] = None 
    deleted_by: Optional[int] = None


class TaskUpdate(BaseModel):
    task_title: Optional[str] = None
    resolved_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    assignee: Optional[int] = None
    project_id: Optional[int] = None
    sprint: Optional[int] = None
    workflowstage_id: Optional[int] = None
    # estimate_time: Optional[str] = None
    created: Optional[int] = None
    deleted_by: Optional[int] = None
    