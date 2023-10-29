from apps.project.models import *
from config.settings import *
from fastapi import APIRouter





Base.metadata.create_all(bind=engine)

router = APIRouter()




@router.get("/endpoint2")
def endpoint2():
    return {"message": "This is endpoint 2 from view2 in folder2"}


