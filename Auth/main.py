from apps.account.views import router as router1
from fastapi import FastAPI
from apps.project.views import router as router2

app = FastAPI()



app.include_router(router1, prefix="/account", tags=["account"])
app.include_router(router2, prefix="/project", tags=["project"])
