import os
import subprocess
import sys
try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    print("\033[91m[SETUP]\033[0m tkinter is not installed. On Linux, try: sudo apt-get install python3-tk")
    exit()

print("\033[92m[SETUP]\033[0m Выбрать директорию со скриптами? [Y/N]")

choice = input().strip().lower()

if choice != "y":
    print("\033[91m[SETUP]\033[0m Выход.")
    exit()

# Диалог выбора папки
root = tk.Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

if not folder_selected:
    print("\033[91m[SETUP]\033[0m Папка не выбрана. Завершение.")
    exit()

print("\033[92m[SETUP]\033[0m Папка выбрана.")

os.chdir(folder_selected)

# Проверка активного скрипта
scripts = [f for f in os.listdir() if f.endswith(".py")]
current_script = os.path.basename(__file__)
if current_script in scripts:
    scripts.remove(current_script)

if not scripts:
    print("\033[91m[SETUP]\033[0m В папке нет Python-скриптов.")
    exit()

# Выводим список скриптов
print("\n\033[96m[SETUP]\033[0m Доступные скрипты:")
for idx, script in enumerate(scripts, 1):
    print(f" {idx}. {script}")

# Запрашиваем выбор
while True:
    try:
        selection = int(input("\n\033[92m[SETUP]\033[0m Выберите номер скрипта для запуска: "))
        if 1 <= selection <= len(scripts):
            break
        else:
            print("\033[91m[SETUP]\033[0m Неверный номер.")
    except ValueError:
        print("\033[91m[SETUP]\033[0m Введите число.")

selected_script = scripts[selection - 1]

# Подтверждение
print(f"\n\033[92m[SETUP]\033[0m Запуск {selected_script}...")
# Запуск выбранного скрипта
subprocess.run([sys.executable, selected_script])