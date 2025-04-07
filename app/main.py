from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import os
from PIL import Image
import uuid

app = FastAPI()

# Создаем таблицы при старте
models.Base.metadata.create_all(bind=engine)

# Директория для сохранения изображений
FACE_IMAGES_DIR = "static/faces"
os.makedirs(FACE_IMAGES_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add-person")
async def add_person(
    full_name: str = Form(...),
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Генерируем уникальное имя файла
    file_ext = face_image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(FACE_IMAGES_DIR, filename)

    # Сохраняем изображение
    try:
        with Image.open(face_image.file) as img:
            img.save(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Сохраняем в БД
    db_person = models.Person(
        full_name=full_name,
        face_image_path=file_path
    )
    
    try:
        db.add(db_person)
        db.commit()
        db.refresh(db_person)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Name already exists")

    return {"status": "success", "person_id": db_person.id}


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/people")
async def get_people(db: Session = Depends(get_db)):
    people = db.query(models.Person).all()
    return [
        {"full_name": p.full_name, 
         "face_image_path": p.face_image_path}
        for p in people
    ]