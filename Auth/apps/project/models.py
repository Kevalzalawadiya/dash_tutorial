from sqlalchemy import Column, Integer, String, Boolean, DateTime, func,ForeignKey
from config.settings import Base
from .models import User
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship



class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False,max_length=32)
    short_name = Column(String, nullable=False,max_length=3)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    manage_by = Column(Integer, ForeignKey(User, ondelete='CASCADE'))
    recipient = Column(ARRAY(String(length=255), dimensions=1), nullable=True)
    user = relationship("User", back_populates="projects")

    workflowstages = relationship("WorkFlowStages", back_populates="project_name")
    projectdevelopers = relationship("ProjectDeveloper", back_populates="project_name")  
    tasks = relationship("Tasks", back_populates="project_name")








class WorkFlowStages(Base):
    __tablename__ = "workflowstages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project = Column(Integer, ForeignKey(Project, ondelete='CASCADE'))


    project_name = relationship("Project", back_populates="workflowstages")
    Tasks = relationship("Tasks", back_populates="workflowstages")



class Role(Base):
    __tablename__ = "roles"

    id =Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    can_create_task = Column(Boolean, default=False)

    projectdevelopers = relationship("ProjectDeveloper", back_populates="roles")



class ProjectDeveloper(Base):
    __tablename__ = "projectdevelopers"

    id = Column(Integer, primary_key=True, index=True)
    project = Column(Integer, ForeignKey(Project, ondelete='CASCADE'))
    created = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    developer = Column(Integer, ForeignKey(User, ondelete='CASCADE'))
    role = Column(Integer, ForeignKey(Role, ondelete='CASCADE'))

    project_name = relationship("Project", back_populates="projectdevelopers")
    user = relationship("User", back_populates="projectdevelopers")
    roles = relationship("Role", back_populates="projectdevelopers")


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    tasks = relationship("Tasks", back_populates="sprints")
  

class Tasks(Base):
    __tablename__ = "tasks"


    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime,nullable=True)
    estimate_time = Column(Boolean,max_length=6, default='00:00')
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime,nullable=True,blank=True)
    assignee = Column(Integer, ForeignKey(User, ondelete='CASCADE'))
    project = Column(Integer, ForeignKey(Project, ondelete='CASCADE'))
    sprint = Column(Integer, ForeignKey(Sprint, ondelete='CASCADE')) 
    stage = Column(Integer, ForeignKey(WorkFlowStages, ondelete='CASCADE'))
    created = Column(Integer, ForeignKey(User, ondelete='CASCADE'))
    deleted_by = Column(Integer, ForeignKey(User,ondelete='SET NULL'),nullable=True)

     

    user = relationship("User", back_populates="tasks")
    project_name = relationship("Project", back_populates="tasks")
    sprints = relationship("Sprint", back_populates="tasks")
    workflowstages = relationship("WorkFlowStages", back_populates="tasks")
    user_create = relationship("User", back_populates="tasks_create")
    user_deleted_by = relationship("User", back_populates="tasks_deleted_by")





class TaskPlanner(Base):
    __tablename__ = "taskplanner"

    STATUS = (
        ("new", "Inactive"),
        ("in_progress", "In progress"),
        ("complete", "Completed")
    )
    PRIORITIES = (
        (1, "Eliminate"),
        (2, "Delegate"),
        (3, "Plan"),
        (4, "Do"),
    )
    title = Column(String,nullable=False)
    priority = Column(Integer,default=1,choices=PRIORITIES)
    status = Column(String,max_length=6,choices=STATUS)
    created = Column(DateTime, default=func.now())
    user = Column(Integer, ForeignKey(User, ondelete='CASCADE'))

    user_name = relationship("User", back_populates="taskplanner")











