from apps.account.views import router as router1
from fastapi import FastAPI
from apps.project.views import project_router 
import uvicorn

app = FastAPI()



app.include_router(router1, prefix="/account", tags=["account"])
app.include_router(project_router, prefix="/project", tags=["project"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)


