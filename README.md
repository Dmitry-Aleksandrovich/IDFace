# Система распознавания лиц с оповещением в Telegram

## 📌 Описание проекта

Курсовой проект представляет собой систему для распознавания лиц с веб-интерфейсом, базой данных для хранения эмбеддингов и интеграцией с Telegram.

Система включает:

- Backend на FastAPI
- Распознавание лиц с помощью `face_recognition`
- Хранение эмбеддингов в PostgreSQL
- Docker и docker-compose для изоляции сервисов
- Telegram-бот для оповещений

---

## 🧠 Стек технологий

- Python 3.9
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker / Docker Compose
- OpenCV
- face_recognition
- Telegram Bot API
- Jinja2
- HTML / CSS / JS

---

## 🗂️ Структура проекта

```
project/
├── app/                    # Backend-приложение FastAPI
│   ├── main.py             # Основной API
│   ├── models.py           # Модель БД
│   ├── database.py         # Подключение к БД
│   ├── templates/          # HTML-шаблоны
│   ├── static/             # Стили и JS
│   ├── Dockerfile          # Dockerfile для backend
│   └── requirements.txt    # Зависимости Python
├── camera/                 # Клиентская часть с камерой
│   └── camera_app.py       # Отправка кадров с камеры
├── static/faces/           # Загруженные изображения лиц
├── bd_face/                # Снимки для примеров
├── fast-create-db.sh       # Скрипт для создания БД
├── docker-compose.yml      # Компоновка сервисов
└── README.md               # Документация (этот файл)
```

---

## ⚙️ Запуск проекта

### 1. Клонируй репозиторий

```bash
git clone https://gitlab.com/gersimok/diplom-spo.git
cd face-recognition-app
```

### 2. Создай `.tg_key.env` файл

```env
telegram_bot_token=your_telegram_token
telegram_chat_id=your_telegram_chat_id
```

### 3. Запусти систему

```bash
docker-compose up --build
```

### 4. Камера

```bash
python3 camera/camera_app.py
```

---

## 🌐 Эндпоинты API

| Метод | URL               | Описание                      |
|-------|-------------------|-------------------------------|
| POST  | /add-person       | Добавление человека           |
| POST  | /search-face      | Поиск лица                    |
| GET   | /                 | Главная страница (ввод лица)  |
| GET   | /search           | Поиск по изображению          |
| GET   | /people           | Получение всех лиц            |

---

## 📸 Алгоритм работы

1. Камера делает снимки каждые 5 секунд
2. Отправляет их на `/search-face`
3. Если лицо не найдено в базе — отправляется Telegram-оповещение с IP, именем хоста и временем

---

## 📬 Пример Telegram-уведомления

```
🔒 Оповещение!
Неизвестное лицо обнаружено

Unix-время: 1713148735
Локальное время: 2025-04-15 16:58:55
IP-адрес: 192.168.1.15
Доменное имя: dmitry-lab.local
```

---

## 🔒 Безопасность

- Все эмбеддинги лиц хранятся в виде JSON-строк
- Уникальность лиц обеспечивается по имени
- Пороговое значение расстояния можно изменить в коде (`threshold = 0.6`)

---

## 📚 Полезные команды

Запуск FastAPI вручную (без Docker):

```bash
uvicorn app.main:app --reload
```

---

## 🧪 TODO / Идеи для улучшения

- Добавить хранение временных меток входа
- Реализовать регистрацию и аутентификацию
- Перейти на GPU-ускорение для face_recognition
- Поддержка потокового видео

---

## 🧑‍💻 Автор

**Дмитрий Павленко Александрович**  
Курс: 4 спо  
Специальность: Информационные системы и программирование  
Email: dmitry.pavlenko.2005@bk.ru

---

## 📝 Лицензия

MIT License