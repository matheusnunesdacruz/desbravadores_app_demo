from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.main import templates
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/fotos", response_class=HTMLResponse)
def fotos_list(request: Request):
    files = os.listdir(UPLOAD_DIR)
    return templates.TemplateResponse("fotos.html", {"request": request, "files": files})

@router.post("/fotos")
async def fotos_add(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse("/fotos", status_code=303)

@router.post("/fotos/{filename}/delete")
def fotos_delete(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return RedirectResponse("/fotos", status_code=303)
