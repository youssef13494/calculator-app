import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Add logging
print(f"BASE_DIR: {BASE_DIR}")
print(f"Static directory exists: {(BASE_DIR / 'static').exists()}")
print(f"CSS file exists: {(BASE_DIR / 'static' / 'style.css').exists()}")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in static: {list((BASE_DIR / 'static').iterdir()) if (BASE_DIR / 'static').exists() else 'Directory not found'}")

app = FastAPI()

# Static files with absolute path
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

# Templates with absolute path
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    num1: float = Form(...),
    num2: float = Form(...),
    operation: str = Form(...)
):
    if operation == "add":
        result = num1 + num2
    elif operation == "sub":
        result = num1 - num2
    elif operation == "mul":
        result = num1 * num2
    elif operation == "div":
        result = "Cannot divide by zero" if num2 == 0 else num1 / num2
    else:
        result = "Invalid operation"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "num1": num1,
            "num2": num2,
            "operation": operation
        }
    )
