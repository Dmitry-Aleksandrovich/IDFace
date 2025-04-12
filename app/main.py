import numpy as np
import face_recognition
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import os
import uuid
from PIL import Image

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

@app.post("/search-face")
async def search_face(
    face_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Вычисляем embedding для входного изображения
    try:
        face_image.file.seek(0)
        input_img = face_recognition.load_image_file(face_image.file)
        input_encodings = face_recognition.face_encodings(input_img)
        if not input_encodings:
            raise HTTPException(status_code=400, detail="No face found in the uploaded image")
        input_encoding = input_encodings[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing input image: {e}")

    # Сравниваем с каждым лицом в базе
    persons = db.query(models.Person).all()
    results = []
    for person in persons:
        try:
            db_img = face_recognition.load_image_file(person.face_image_path)
            db_encodings = face_recognition.face_encodings(db_img)
            if not db_encodings:
                continue  # если лицо не обнаружено, пропускаем запись
            db_encoding = db_encodings[0]
            distance = np.linalg.norm(input_encoding - db_encoding)
            results.append({
                "person_id": person.id,
                "full_name": person.full_name,
                "face_image_path": person.face_image_path,
                "distance": distance
            })
        except Exception as e:
            continue  # если ошибка при обработке конкретного изображения, пропускаем

    # Задаем порог совпадения (например, 0.6)
    threshold = 0.6
    matches = [r for r in results if r["distance"] < threshold]
    matches = sorted(matches, key=lambda r: r["distance"])

    return {"matches": matches, "all_results": results}

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Новый эндпоинт для отображения страницы поиска лица
@app.get("/search")
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/people")
async def get_people(db: Session = Depends(get_db)):
    people = db.query(models.Person).all()
    return [
        {"full_name": p.full_name, 
         "face_image_path": p.face_image_path}
        for p in people
    ]

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
