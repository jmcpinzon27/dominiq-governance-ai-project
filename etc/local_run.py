import os

from fastapi import FastAPI, Request

from agent_management.adapters.fastapi.mangum_adapter import router as agent_management_router
import agent_management

app = FastAPI()


app.include_router(agent_management_router, prefix="/agent_management", tags=["items"])

@app.middleware("http")
async def set_pythonpath_middleware(request: Request, call_next):

    # Set the PYTHONPATH based on the path
    if request.url.path.startswith("/agent_management"):
        os.environ["PYTHONPATH"] = f'{os.environ["PYTHONPATH"]}:{os.path.dirname(os.path.abspath(agent_management.__file__))}'
    # elif path.startswith("/project1"):
    #     os.environ["PYTHONPATH"] = "path/to/your/folder1"  # Adjust the path accordingly
    # elif path.startswith("/project2"):
    #     os.environ["PYTHONPATH"] = "path/to/your/folder2"  # Adjust the path accordingly
    # else:
    #     return {"error": "Invalid project path"}

    # Call the next middleware or endpoint
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
