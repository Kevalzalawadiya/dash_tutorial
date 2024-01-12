from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table,func,Enum,ARRAY
from sqlalchemy.orm import relationship,validates
from config.settings import *
# from apps.account.models import User


# association_table = Table('association', Base.metadata,
#                          Column('project_id', Integer, ForeignKey('projects.id')),
#                          Column('developer_id', Integer, ForeignKey('projectdevelopers.id'))
#                          )

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    short_name = Column(String(length=10), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    # recipient = Column(ARRAY(String), nullable=True)
    manage_by = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'))
    

    user_mangeby=relationship("User",back_populates="project")
    # developer=relationship("ProjectDeveloper",secondary=association_table,back_populates="project")
    # workflowstages=relationship("WorkFlowStages",back_populates="projects")
    # projectdevelopers=relationship("ProjectDeveloper",back_populates="projects")
   

# class WorkFlowStages(Base):
#     __tablename__ = "workflowstages"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     project_id=Column(Integer,ForeignKey('projects.id',ondelete='CASCADE'))


#     projects=relationship("Project",back_populates="workflowstages")
#     tasks = relationship('Task', back_populates='workflow_stage')

    

# class Role(Base):
#     __tablename__ = "roles"
#     id =Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     can_create_task = Column(Boolean, default=False)
    
#     projectdevelopers=relationship("ProjectDeveloper",back_populates="roles")
   
   
# class ProjectDeveloper(Base):
#     __tablename__ = "projectdevelopers"

#     id = Column(Integer, primary_key=True, index=True)
#     created = Column(DateTime, default=func.now())
#     is_active = Column(Boolean, default=True)
#     project_id=Column(Integer,ForeignKey('projects.id',ondelete='CASCADE'))
#     developer=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
#     role_id=Column(Integer,ForeignKey('roles.id',ondelete='CASCADE'))

#     project=relationship("Project",secondary=association_table,back_populates="developer")
#     projects=relationship("Project",back_populates="projectdevelopers")
#     users=relationship("User",back_populates="projectdevelopers")
#     roles=relationship("Role",back_populates="projectdevelopers")




# class Tasks(Base):
#     __tablename__ = "task"
#     id = Column(Integer, primary_key=True, index=True)
#     task_title = Column(String, nullable=False)
#     created_at = Column(DateTime, default=func.now())
#     resolved_at = Column(DateTime, nullable=True)
#     estimate_time = Column(String, default='00:00')
#     is_deleted = Column(Boolean, default=False)
#     deleted_at = Column(DateTime, nullable=True)
#     created_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
#     assignee_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
#     project_id=Column(Integer,ForeignKey('projects.id',ondelete='CASCADE'))
#     stage_id=Column(Integer,ForeignKey('workflowstages.id',ondelete='CASCADE'))
#     deletedby_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
#     sprint_id=Column(Integer,ForeignKey('sprints.id',ondelete='CASCADE'))

#     users=relationship("User",back_populates="task")
#     users=relationship("User",back_populates="task")
#     project = relationship('Project', back_populates='tasks')
#     workflow_stage = relationship('WorkFlowStages', back_populates='tasks')
#     users=relationship("User",back_populates="task")
#     sprints=relationship("Sprint",back_populates="task")


# class Sprint(Base):
#     __tablename__ = "sprints"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     start_date = Column(DateTime, nullable=False)
#     end_date = Column(DateTime, nullable=False)

#     task=relationship("Task",back_populates="sprints")





# class TaskPlanner(Base):
#     __tablename__ = "taskplanner"

#     STATUS = {"new": "Inactive", "in_progress": "In progress", "complete": "Completed"}
#     PRIORITIES = {1: "Eliminate", 2: "Delegate", 3: "Plan", 4: "Do"}

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     priority = Column(Integer, default=1)
#     status = Column(String(6))
#     created = Column(DateTime, default=func.now())
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

#     users=relationship("User",back_populates="taskplanner")

#     @validates('priority')
#     def validate_priority(self, key, value):
#         if value not in self.PRIORITIES:
#             raise ValueError(f"Invalid priority value: {value}")
#         return value

#     @validates('status')
#     def validate_status(self, key, value):
#         if value not in self.STATUS:
#             raise ValueError(f"Invalid status value: {value}")
#         return value