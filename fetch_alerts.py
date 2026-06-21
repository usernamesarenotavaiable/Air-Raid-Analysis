import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any

def fetch_and_save_alerts(api_token: str) -> Optional[Dict[str, Any]]:
    """
    Виконує GET-запит до alerts.in.ua API та зберігає сирий JSON-дамп локально.
    """
    api_url = "https://api.alerts.in.ua/v1/alerts/active.json"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    # Визначення шляхів збереження
    data_dir = Path("data")
    file_path = data_dir / "raw_alerts.json"
    
    # Створення папки data/, якщо вона не існує
    data_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Виконання запиту із захистом від зависання (timeout=15)
        response = requests.get(api_url, headers=headers, timeout=15)
        
        # Перевірка на HTTP-помилки (наприклад, 401 Unauthorized, 500 Server Error)
        response.raise_for_status()
        
        # Парсинг відповіді
        data = response.json()
        
        # Збереження "сирих" даних
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        print(f"Успіх: Дані збережено до {file_path}")
        return data
        
    except requests.exceptions.ConnectionError:
        print("Помилка: Відсутнє підключення до мережі або DNS не знайдено.")
    except requests.exceptions.Timeout:
        print("Помилка: Сервер не відповів за 15 секунд (Timeout).")
    except requests.exceptions.HTTPError as http_err:
        print(f"Помилка сервера або авторизації: {http_err}")
    except json.JSONDecodeError:
        print("Помилка: Отримано невалідний JSON.")
    except Exception as e:
        print(f"Критична помилка виконання: {e}")
        
    return None

if __name__ == "__main__":
    # Твій актуальний токен
    API_TOKEN = "8d278fc4c3046c3341a2d3ae81d5d6648be741d6ab2203"
    
    # Виклик функції для завантаження даних
    raw_data = fetch_and_save_alerts(API_TOKEN)