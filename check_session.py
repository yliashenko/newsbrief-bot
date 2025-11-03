#!/usr/bin/env python3
"""
Швидка перевірка валідності Telegram user session
"""
import asyncio
import sys
from pathlib import Path
from bot.telegram_client import client, check_session_validity, close_client

session_file = Path("user_session.session")

print("🔍 Перевірка поточної сесії...\n")
print(f"📁 Файл сесії: {session_file.absolute()}")
print(f"📄 Файл існує: {'✅ Так' if session_file.exists() else '❌ Ні'}")

if not session_file.exists():
    print("\n❌ Файл сесії не знайдено!")
    print("💡 Потрібно створити нову сесію")
    print("\nЩоб створити нову сесію:")
    print("   1. Запустіть: python3 main.py")
    print("   2. Коли запитає 'Please enter your phone (or bot token):'")
    print("   3. Введіть свій НОМЕР ТЕЛЕФОНУ (не bot token!), формат: +380XXXXXXXXX")
    print("   4. Введіть код з Telegram")
    sys.exit(1)

async def check():
    try:
        result = await check_session_validity()
        
        if result.get("is_bot"):
            print("\n" + "=" * 60)
            print("❌ ПРОБЛЕМА: Сесія авторизована як БОТ!")
            print(f"\n👤 Інформація:")
            print(f"   • ID: {result['user_id']}")
            if result["username"]:
                print(f"   • Username: @{result['username']}")
            
            print("\n" + "=" * 60)
            print("🚨 ПОТРІБНО ПЕРЕГЕНЕРУВАТИ СЕСІЮ!")
            print("\n💡 Як виправити:")
            print("   1. Видаліть файл user_session.session:")
            print("      rm user_session.session")
            print("   2. Запустіть бота: python3 main.py")
            print("   3. Коли запитає 'Please enter your phone (or bot token):'")
            print("      ↳ Введіть свій НОМЕР ТЕЛЕФОНУ (не bot token!)")
            print("      ↳ Формат: +380XXXXXXXXX")
            print("   4. Введіть код, який прийде в Telegram")
            print("   5. Після успішної авторизації файл сесії буде створено")
            return False
        elif result["is_valid"]:
            print("\n" + "=" * 60)
            print("✅ Сесія валідна та працює правильно!")
            print(f"\n👤 Інформація про користувача:")
            print(f"   • ID: {result['user_id']}")
            if result["username"]:
                print(f"   • Username: @{result['username']}")
            print("\n✅ Перегенерувати сесію НЕ потрібно")
            return True
        else:
            print("\n" + "=" * 60)
            print("❌ Сесія не валідна!")
            if result["error"]:
                print(f"   Помилка: {result['error']}")
            print("\n💡 Потрібно перегенерувати сесію")
            print("   1. Видаліть файл: rm user_session.session")
            print("   2. Запустіть: python3 main.py")
            print("   3. Введіть номер телефону (не bot token!)")
            return False
            
    except Exception as e:
        print(f"\n❌ Помилка при перевірці: {e}")
        return False
    finally:
        await close_client()

try:
    result = asyncio.run(check())
    sys.exit(0 if result else 1)
except KeyboardInterrupt:
    print("\n\n⚠️  Перевірку перервано")
    sys.exit(1)

