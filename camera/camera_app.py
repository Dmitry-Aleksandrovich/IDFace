import cv2
import time
import requests

# URL для эндпоинта /search-face
url = "http://localhost:8000/search-face"  # при необходимости замените на актуальный адрес

# Инициализация веб-камеры
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось открыть камеру")
    exit()

print("Запуск захвата кадров с камеры каждые 5 секунд...")
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр с камеры")
            break

        # Кодируем кадр в JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Ошибка кодирования изображения")
            continue

        # Получаем байты изображения
        image_bytes = buffer.tobytes()

        # Формируем данные для отправки
        files = {
            "face_image": ("camera.jpg", image_bytes, "image/jpeg")
        }

        try:
            response = requests.post(url, files=files)
            # Пытаемся получить JSON с результатами
            data = response.json()
            print("Ответ сервера:", data)
        except Exception as e:
            print("Ошибка при отправке или получении ответа:", e)

            cv2.imshow("Камера", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Пауза 5 секунд перед следующей итерацией
        time.sleep(5)
except KeyboardInterrupt:
    print("Остановка приложения...")
finally:
    cap.release()
