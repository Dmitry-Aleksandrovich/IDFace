import cv2
import time
import requests
import face_recognition
import telegram
import asyncio
import socket
import os

from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path=".tg_key.env")

#token your tg bot 
telegram_bot_token = os.getenv("telegram_bot_token")

#your tg chat id
telegram_chat_id = os.getenv("telegram_chat_id")

# Получение IP-адреса и доменного имени
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS — просто для выбора интерфейса
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Не удалось определить"

hostname = socket.gethostname()
local_ip = get_local_ip()
domain_name = socket.getfqdn()



# URL для эндпоинта /search-face
telegram_chat_id = os.getenv("url")
# как пример url = "http://localhost:8000/search-face"

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

            current_unix_time = int(time.time())
            readable_time = datetime.fromtimestamp(current_unix_time).strftime("%Y-%m-%d %H:%M:%S")

            # Общая часть для любого сообщения
            time_info = (
                f"Unix-время: {current_unix_time}\n"
                f"Локальное время: {readable_time}\n"
                f"IP-адрес: {local_ip}\n"
                f"Доменное имя: {domain_name}"
            )

            if data.get("matches"):
                for match in data["matches"]:
                    print(f"Найдено совпадение с: {match}")
                    message = f"🔒 Оповещение!\nНайдено лицо в базе данных: {match}\n{time_info}"
                    send_telegram_alert(message)
            else:
                print("Лицо не найдено в базе данных")
                message = f"⚠️ Обнаружено новое лицо, отсутствующее в базе данных!\n{time_info}"
                send_telegram_alert(message)

        except Exception as e:
            print("Ошибка при отправке или получении ответа:", e)



        except Exception as e:
            print("Ошибка при отправке или получении ответа:", e)


        # Пауза 5 секунд перед следующей итерацией
        time.sleep(5)

except KeyboardInterrupt:
    print("Остановка приложения...")
finally:
    cap.release()
    cv2.destroyAllWindows()
