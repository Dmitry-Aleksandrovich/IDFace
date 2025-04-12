import cv2
import time
import requests
import face_recognition
import telegram
import asyncio

# URL для эндпоинта /search-face
url = "http://localhost:8000/search-face"

# Telegram bot settings
telegram_bot_token = '7873745697:AAGTzIzKV0iTkZh2JWBsydHK61FKb-TbOkU'  # Вставьте свой токен
telegram_chat_id = '743292242'  # Вставьте свой chat_id (можно получить через @userinfobot)

# Инициализация бота
bot = telegram.Bot(token=telegram_bot_token)

# Инициализация веб-камеры
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось открыть камеру")
    exit()

print("Запуск захвата кадров с камеры каждые 5 секунд...")

def send_telegram_alert(message):
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    try:
        response = requests.post(telegram_api_url, data=data)
        if response.status_code != 200:
            print(f"Ошибка Telegram API: {response.text}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")


try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр с камеры")
            break

        # Показываем изображение, чтобы видеть кадр
        #cv2.imshow("Камера", frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

        # Преобразуем кадр в RGB для face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        print(f"Найдено лиц: {len(face_locations)}")

        if not face_locations:
            print("Лицо не обнаружено на текущем кадре, пропуск отправки")
            time.sleep(5)
            continue

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
            data = response.json()
            print("Ответ сервера:", data)

            # Если найдено совпадение в базе
            if data.get("matches"):
                for match in data["matches"]:
                    print(f"Найдено совпадение с: {match}")
                    message = f"Оповещение! Найдено лицо в базе данных: {match}"
                    send_telegram_alert(message)
            else:
                print("Лицо не найдено в базе данных")
                message = "Оповещение! Обнаружено новое лицо, отсутствующее в базе данных!"
                send_telegram_alert(message)

        except Exception as e:
            print("Ошибка при отправке или получении ответа:", e)


        # Пауза 5 секунд перед следующей итерацией
        time.sleep(5)

except KeyboardInterrupt:
    print("Остановка приложения...")
finally:
    cap.release()
    cv2.destroyAllWindows()
