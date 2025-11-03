#!/usr/bin/env python3
"""
Скрипт для перевірки який саме GROQ_API_KEY завантажується
"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("🔍 Діагностика завантаження GROQ_API_KEY...\n")

# Перевірка .env файлу
env_path = Path(".env")
if env_path.exists():
    print(f"✅ Файл .env знайдено: {env_path.absolute()}")
    with open(env_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if 'GROQ_API_KEY' in line and '=' in line:
                key_part = line.split('=', 1)[1].strip()
                print(f"📄 В .env файлі (рядок {line_num}):")
                print(f"   Початок: {key_part[:12]}...")
                print(f"   Кінець: ...{key_part[-12:]}")
                print(f"   Довжина: {len(key_part)} символів")
else:
    print("❌ Файл .env не знайдено")

print("\n" + "=" * 60)

# Перевірка змінних середовища ПЕРЕД load_dotenv
env_before = os.getenv("GROQ_API_KEY")
if env_before:
    print(f"⚠️  GROQ_API_KEY вже встановлено в системних змінних (ПЕРЕД load_dotenv):")
    print(f"   Початок: {env_before[:12]}...")
    print(f"   Довжина: {len(env_before)} символів")
else:
    print("✅ GROQ_API_KEY не встановлено в системних змінних (ПЕРЕД load_dotenv)")

print("\n" + "=" * 60)

# Завантажуємо .env
print("📥 Завантаження .env файлу...")
load_dotenv()

# Перевірка після load_dotenv
key_after = os.getenv("GROQ_API_KEY")
if key_after:
    print(f"✅ GROQ_API_KEY після load_dotenv:")
    print(f"   Початок: {key_after[:12]}...")
    print(f"   Кінець: ...{key_after[-12:]}")
    print(f"   Довжина: {len(key_after)} символів")
    print(f"   Без пробілів: {key_after.strip()[:12]}...")
    
    # Перевірка на різницю
    if env_before and env_before != key_after:
        print("\n⚠️  УВАГА: Ключ з системних змінних відрізняється від ключа з .env!")
        print(f"   Системний: {env_before[:12]}...")
        print(f"   З .env: {key_after[:12]}...")
        print("\n💡 Системні змінні мають пріоритет над .env файлом!")
else:
    print("❌ GROQ_API_KEY не завантажився після load_dotenv")

print("\n" + "=" * 60)
print("📋 Імпорт з config.py...")

# Перевірка що імпортується з config
try:
    from config import GROQ_API_KEY as config_key
    print(f"✅ GROQ_API_KEY з config.py:")
    print(f"   Початок: {config_key[:12]}...")
    print(f"   Кінець: ...{config_key[-12:]}")
    print(f"   Довжина: {len(config_key)} символів")
except Exception as e:
    print(f"❌ Помилка імпорту: {e}")

