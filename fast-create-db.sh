#!/bin/bash
#скрипт для быстрого добавления изображений в бд для тестов


# Каталог с изображениями
IMAGES_DIR="bd_face"
# URL конечной точки API
ENDPOINT="http://localhost:8000/add-person"

# Обход файлов в каталоге
for FILE in "$IMAGES_DIR"/*; do
    # Фильтруем файлы по расширению
    if [[ "$FILE" =~ \.(png|jpg|jpeg|gif)$ ]]; then
        # Получаем имя файла без расширения
        BASENAME=$(basename "$FILE")
        FULL_NAME="${BASENAME%.*}"
        
        echo "Отправка файла: $FILE, full_name: $FULL_NAME"

        # Отправка POST-запроса с использованием curl:
        curl -X POST "$ENDPOINT" \
            -F "full_name=$FULL_NAME" \
            -F "face_image=@$FILE" \
            --max-time 10

        echo -e "\n"
    fi
done
