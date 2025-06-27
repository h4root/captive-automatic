import requests
import os
import time
import warnings
import json
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter("ignore", InsecureRequestWarning)
print("\033[93m[INFO]\033[0m Проверка SSL выключена.")

CONFIG_FILE = "config.json"
PLACEHOLDER_VALUES = {
    "login": "yourlogin",
    "password": "yourpassword",
    "auth_url": "https://yoururl/auth.php"
}

def ensure_protocol(config_path="config.json"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"\033[91m[FAIL]\033[0m Ошибка загрузки config.json: {e}")
        exit()

    url = config.get("auth_url", "")
    if not (url.startswith("http://") or url.startswith("https://")):
        print(f"\033[93m[INFO]\033[0m В URL отсутствует протокол:\n  {url}")
        while True:
            proto = input("Добавить протокол (1 - https, 2 - http): ").strip()
            if proto == "1":
                url = "https://" + url
                break
            elif proto == "2":
                url = "http://" + url
                break
            else:
                print("Введите 1 или 2.")
        config["auth_url"] = url
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print(f"\033[92m[OK]\033[0m Протокол добавлен и сохранён: {url}")
    return config

def config_valid(config):
    for key, placeholder in PLACEHOLDER_VALUES.items():
        if key not in config or not config[key] or config[key] == placeholder:
            return False
    return True

def create_config():
    print("\033[93m[SETUP]\033[0m Конфигурационный файл не найден или заполнен некорректно.")
    login = input("Введите логин: ").strip()
    password = input("Введите пароль: ").strip()
    auth_url = input("Введите URL авторизации: ").strip()

    config = {
        "login": login,
        "password": password,
        "auth_url": auth_url
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print("\033[92m[SETUP]\033[0m Конфигурационный файл создан.")

def load_or_create_config():
    if not os.path.exists(CONFIG_FILE):
        create_config()
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    else:
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            if not config_valid(config):
                create_config()
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
            return config
        except Exception:
            create_config()
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config

config = load_or_create_config()
config = ensure_protocol("config.json")

def is_connected():
    try:
        requests.get("https://www.google.ru", timeout=3)
        return True
    except:
        return False

def authorize():
    print("\033[92m[OK]\033[0m Авторизация...")
    payload = {
        'url': config["auth_url"],
        'login': config["login"],
        'passwd': config["password"]
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.post(config["auth_url"], data=payload, headers=headers, verify=False)
        if "Неверный логин или пароль" in response.text or response.status_code != 200:
            print("\033[91m[FAIL]\033[0m Ошибка авторизации.")
        else:
            print("\033[92m[OK]\033[0m Авторизация прошла успешно.")
    except Exception as e:
        print(f"\033[91m[FAIL]\033[0m Не удалось отправить запрос: {e}")

# основной цикл
while True:
    if not hasattr(authorize, "counter"):
        authorize.counter = 0
    authorize.counter += 1
    if authorize.counter >= 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[93m[INFO]\033[0m Проверка SSL выключена.")
        authorize.counter = 0
    if is_connected():
        print(f"\033[92m[STATUS] {time.strftime('%H:%M:%S')} \033[0m Сеть стабильна.")
    else:
        print("\033[91m[FAIL]\033[0m Соединение потеряно, повторная авторизация...")
        authorize()