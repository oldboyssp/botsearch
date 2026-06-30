# ═══════════════════════════════════════════════════════════════════════════════════════
# ╔═════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                     ║
# ║   ██████╗ ██╗██╗  ██╗    ██████╗ ██████╗  ██████╗ ██████╗ ██╗██╗   ██╗            ║
# ║   ██╔══██╗██║╚██╗██╔╝    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║██║   ██║            ║
# ║   ██║  ██║██║ ╚███╔╝     ██████╔╝██████╔╝██║   ██║██████╔╝██║██║   ██║            ║
# ║   ██║  ██║██║ ██╔██╗     ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██║╚██╗ ██╔╝            ║
# ║   ██████╔╝██║██╔╝ ██╗    ██║     ██║  ██║╚██████╔╝██████╔╝██║ ╚████╔╝             ║
# ║   ╚═════╝ ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝              ║
# ║                                                                                     ║
# ║   DIX PROBIV BOT v5.0 — ПОЛНАЯ ВЕРСИЯ БЕЗ СОКРАЩЕНИЙ                               ║
# ║   Проект #Амнезия | Команда Dixyi | 13.10.2025                                      ║
# ║                                                                                     ║
# ╚═════════════════════════════════════════════════════════════════════════════════════╝
# ═══════════════════════════════════════════════════════════════════════════════════════

import asyncio
import json
import re
import os
import sys
import time
import shutil
import sqlite3
import random
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Any
from typing import Optional
from typing import Set
from typing import Tuple
from collections import defaultdict

from telethon import TelegramClient
from telethon import events
from telethon import Button
from telethon.tl.types import KeyboardButton
from telethon.tl.types import ReplyKeyboardMarkup
from telethon.tl.types import KeyboardButtonRow
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import GetParticipantRequest

import aiohttp
from aiohttp import ClientSession
from aiohttp import ClientTimeout

# ═══════════════════════════════════════════════════════════════════════════════════════
# КОНФИГУРАЦИЯ БОТА
# ═══════════════════════════════════════════════════════════════════════════════════════

API_ID: int = 2040
API_HASH: str = 'b18441a1ff607e10a989891a5462e627'
BOT_TOKEN: str = '8953729393:AAH6SDumg4yzdNgh1l6AZqX39Das7zGg9gM'
OWNER_ID: int = 1913718956
OWNER_USERNAME: str = '@kapolam'
SUBSCRIPTION_CHANNEL: str = '@kepber'

SESSION_PATH: str = '/storage/emulated/0/Download/DIX_SESSION_DATA/searchbot_session'
MIRRORS_FOLDER: str = '/storage/emulated/0/Download/DIX_MIRRORS'
MIRRORS_FILE: str = '/storage/emulated/0/Download/DIX_MIRRORS/mirrors.json'
DATABASE_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/dix_results.db'
WHITELIST_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/dix_whitelist.json'
LOGS_FOLDER: str = '/storage/emulated/0/Download/DIX_LOGS'
ADMINS_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/admins.json'
BANS_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/bans.json'
MUTES_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/mutes.json'

SEARCH_BOT_USERNAME: str = '@sjgdfj0ghjdhjjegtjjebot'

# ═══════════════════════════════════════════════════════════════════════════════════════
# API КЛЮЧИ
# ═══════════════════════════════════════════════════════════════════════════════════════

VK_ACCESS_TOKEN: str = '0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c'
LEAKCHECK_API_KEY: str = '49535f49545f5245414c4c595f4150495f4b4559'
LEAKOSINT_API_KEY: str = '7949201327:7z2O7xWq'
IPINFO_API_KEY: str = '1d26e0613d1988'
SHODAN_API_KEY: str = 'DF7LYF16WVqSCW5C715egWBpnS03y6si'

# ═══════════════════════════════════════════════════════════════════════════════════════
# URL ДЛЯ API ЗАПРОСОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

HTMLWEB_API_URL: str = 'https://htmlweb.ru/geo/api.php?json&telcod={number}'
LEAKCHECK_API_URL: str = 'https://leakcheck.net/api/public?key={key}&check={query}'
LEAKOSINT_API_URL: str = 'https://leakosint.net/api/public?key={key}&check={query}'
IPINFO_API_URL: str = 'https://ipinfo.io/{ip}/json?token={key}'
SHODAN_API_URL: str = 'https://api.shodan.io/shodan/host/{ip}?key={key}'
MACVENDORS_API_URL: str = 'https://api.macvendors.com/{mac}'
VK_API_URL: str = 'https://api.vk.com/method/users.search?access_token={token}&v=5.131&q={query}&fields=first_name,last_name,photo_max_orig'

# ═══════════════════════════════════════════════════════════════════════════════════════
# ИЕРАРХИЯ АДМИНИСТРАТОРОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

ADMIN_LEVEL_NAMES: Dict[int, str] = {
    1: 'Младший модератор',
    2: 'Модератор',
    3: 'Старший модератор',
    4: 'Администратор',
    5: 'Старший администратор',
    6: 'Главный администратор',
    7: 'Владелец'
}

ADMIN_PERMISSIONS: Dict[int, Dict[str, Any]] = {
    1: {
        'max_mute_minutes': 60,
        'daily_requests': 7,
        'can_mute': True,
        'can_warn': False,
        'can_view_stats': False,
        'can_promote_to': 0,
        'can_broadcast': False
    },
    2: {
        'max_mute_minutes': 180,
        'daily_requests': 10,
        'can_mute': True,
        'can_warn': True,
        'can_view_stats': False,
        'can_promote_to': 0,
        'can_broadcast': False
    },
    3: {
        'max_mute_minutes': 300,
        'max_ban_hours': 1,
        'daily_requests': 15,
        'can_mute': True,
        'can_ban': True,
        'can_warn': True,
        'can_view_stats': True,
        'can_promote_to': 0,
        'can_broadcast': False
    },
    4: {
        'max_mute_minutes': 2880,
        'max_ban_hours': 24,
        'daily_requests': 20,
        'can_mute': True,
        'can_ban': True,
        'can_warn': True,
        'can_view_stats': True,
        'can_promote_to': 3,
        'can_broadcast': False
    },
    5: {
        'max_mute_minutes': 4320,
        'max_ban_hours': 72,
        'daily_requests': 50,
        'can_mute': True,
        'can_ban': True,
        'can_warn': True,
        'can_view_stats': True,
        'can_promote_to': 4,
        'can_broadcast': False
    },
    6: {
        'max_mute_minutes': 10080,
        'max_ban_hours': 168,
        'daily_requests': 100,
        'can_mute': True,
        'can_ban': True,
        'can_warn': True,
        'can_view_stats': True,
        'can_promote_to': 5,
        'can_broadcast': True
    },
    7: {
        'max_mute_minutes': 999999,
        'max_ban_hours': 999999,
        'daily_requests': 999999,
        'can_mute': True,
        'can_ban': True,
        'can_warn': True,
        'can_view_stats': True,
        'can_promote_to': 6,
        'can_broadcast': True,
        'is_owner': True
    }
}

# ═══════════════════════════════════════════════════════════════════════════════════════
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ═══════════════════════════════════════════════════════════════════════════════════════

user_states: Dict[int, Optional[str]] = {}

user_limits: Dict[int, Dict[str, Any]] = {}

user_subscriptions: Dict[int, bool] = {}

user_referrals: Dict[int, str] = {}

user_last_message_time: Dict[int, List[float]] = defaultdict(list)

banned_users: Dict[int, Dict[str, Any]] = {}

muted_users: Dict[int, Dict[str, Any]] = {}

admins: Dict[int, Dict[str, Any]] = {}

DAILY_LIMIT: int = 5
REFERRAL_BONUS: int = 1
FLOOD_MESSAGES_LIMIT: int = 20
FLOOD_MUTE_MINUTES: int = 10

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ДЛЯ РАБОТЫ С АДМИНАМИ
# ═══════════════════════════════════════════════════════════════════════════════════════

def load_admins_from_file() -> None:
    global admins
    if not os.path.exists(ADMINS_FILE):
        admins = {
            OWNER_ID: {
                'level': 7,
                'added_by': OWNER_ID,
                'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        save_admins_to_file()
        return
    try:
        with open(ADMINS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            admins = {}
            for key, value in data.items():
                admins[int(key)] = value
    except Exception as error:
        print(f'[ADMINS] Ошибка загрузки: {error}')
        admins = {
            OWNER_ID: {
                'level': 7,
                'added_by': OWNER_ID,
                'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        save_admins_to_file()

def save_admins_to_file() -> None:
    try:
        os.makedirs(os.path.dirname(ADMINS_FILE), exist_ok=True)
        data_to_save = {}
        for key, value in admins.items():
            data_to_save[str(key)] = value
        with open(ADMINS_FILE, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
    except Exception as error:
        print(f'[ADMINS] Ошибка сохранения: {error}')

def get_admin_level(user_id: int) -> int:
    if user_id in admins:
        return admins[user_id].get('level', 0)
    return 0

def is_user_admin(user_id: int) -> bool:
    return get_admin_level(user_id) >= 1

def can_admin_promote_to(admin_user_id: int, target_level: int) -> bool:
    admin_level = get_admin_level(admin_user_id)
    if admin_level >= 7:
        return target_level <= 6
    max_promote_level = ADMIN_PERMISSIONS.get(admin_level, {}).get('can_promote_to', 0)
    return target_level <= max_promote_level

def get_admin_daily_limit(user_id: int) -> int:
    level = get_admin_level(user_id)
    if level >= 1:
        return ADMIN_PERMISSIONS.get(level, {}).get('daily_requests', DAILY_LIMIT)
    return DAILY_LIMIT

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ АНТИ-ФЛУДА
# ═══════════════════════════════════════════════════════════════════════════════════════

def check_user_flood(user_id: int) -> bool:
    current_time = time.time()
    user_last_message_time[user_id].append(current_time)
    user_last_message_time[user_id] = [
        timestamp for timestamp in user_last_message_time[user_id]
        if current_time - timestamp < 1.0
    ]
    if len(user_last_message_time[user_id]) > FLOOD_MESSAGES_LIMIT:
        mute_user(user_id, FLOOD_MUTE_MINUTES, 'Автоматический мут за флуд (более 20 сообщений в секунду)')
        return True
    return False

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ БАНОВ И МУТОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

def load_bans_from_file() -> None:
    global banned_users
    if not os.path.exists(BANS_FILE):
        banned_users = {}
        return
    try:
        with open(BANS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            banned_users = {}
            for key, value in data.items():
                banned_users[int(key)] = value
    except Exception:
        banned_users = {}

def save_bans_to_file() -> None:
    try:
        os.makedirs(os.path.dirname(BANS_FILE), exist_ok=True)
        data_to_save = {}
        for key, value in banned_users.items():
            data_to_save[str(key)] = value
        with open(BANS_FILE, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
    except Exception:
        pass

def load_mutes_from_file() -> None:
    global muted_users
    if not os.path.exists(MUTES_FILE):
        muted_users = {}
        return
    try:
        with open(MUTES_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            muted_users = {}
            for key, value in data.items():
                muted_users[int(key)] = value
    except Exception:
        muted_users = {}

def save_mutes_to_file() -> None:
    try:
        os.makedirs(os.path.dirname(MUTES_FILE), exist_ok=True)
        data_to_save = {}
        for key, value in muted_users.items():
            data_to_save[str(key)] = value
        with open(MUTES_FILE, 'w', encoding='utf-8') as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
    except Exception:
        pass

def ban_user(user_id: int, reason: str = 'Нарушение правил', banned_by: int = OWNER_ID) -> None:
    banned_users[user_id] = {
        'user_id': user_id,
        'reason': reason,
        'banned_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'banned_by': banned_by
    }
    save_bans_to_file()

def unban_user(user_id: int) -> bool:
    if user_id in banned_users:
        del banned_users[user_id]
        save_bans_to_file()
        return True
    return False

def mute_user(user_id: int, minutes: int = 60, reason: str = 'Нарушение правил', muted_by: int = OWNER_ID) -> None:
    mute_until = datetime.now() + timedelta(minutes=minutes)
    muted_users[user_id] = {
        'user_id': user_id,
        'reason': reason,
        'muted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'mute_until': mute_until.strftime('%Y-%m-%d %H:%M:%S'),
        'minutes': minutes,
        'muted_by': muted_by
    }
    save_mutes_to_file()

def unmute_user(user_id: int) -> bool:
    if user_id in muted_users:
        del muted_users[user_id]
        save_mutes_to_file()
        return True
    return False

def is_user_banned(user_id: int) -> bool:
    return user_id in banned_users

def is_user_muted(user_id: int) -> bool:
    if user_id not in muted_users:
        return False
    mute_data = muted_users[user_id]
    mute_until = datetime.strptime(mute_data['mute_until'], '%Y-%m-%d %H:%M:%S')
    if datetime.now() > mute_until:
        del muted_users[user_id]
        save_mutes_to_file()
        return False
    return True

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ПОДПИСКИ И ЛИМИТОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

def check_user_subscription(user_id: int) -> bool:
    if user_id in user_subscriptions:
        return user_subscriptions[user_id]
    if get_admin_level(user_id) >= 1:
        return True
    return False

def get_user_daily_limit(user_id: int) -> int:
    admin_level = get_admin_level(user_id)
    if admin_level >= 1:
        return get_admin_daily_limit(user_id)
    limit = DAILY_LIMIT
    if user_id in user_referrals:
        limit = limit + REFERRAL_BONUS
    if check_user_subscription(user_id):
        limit = 999999
    return limit

def get_user_requests_count_today(user_id: int) -> int:
    today = datetime.now().strftime('%Y-%m-%d')
    if user_id not in user_limits:
        user_limits[user_id] = {'date': today, 'count': 0}
    if user_limits[user_id].get('date') != today:
        user_limits[user_id] = {'date': today, 'count': 0}
    return user_limits[user_id].get('count', 0)

def increment_user_requests_count(user_id: int) -> None:
    today = datetime.now().strftime('%Y-%m-%d')
    if user_id not in user_limits:
        user_limits[user_id] = {'date': today, 'count': 0}
    if user_limits[user_id].get('date') != today:
        user_limits[user_id] = {'date': today, 'count': 1}
    else:
        user_limits[user_id]['count'] = user_limits[user_id].get('count', 0) + 1

def can_user_make_request(user_id: int) -> bool:
    if user_id == OWNER_ID:
        return True
    current_count = get_user_requests_count_today(user_id)
    limit = get_user_daily_limit(user_id)
    return current_count < limit

def generate_referral_link_for_user(user_id: int) -> str:
    return f'https://t.me/antiseach_bot?start=ref{user_id}'

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ЛОГИРОВАНИЯ
# ═══════════════════════════════════════════════════════════════════════════════════════

def write_log_message(level: str, message: str) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_text = f'[{timestamp}] [{level}] {message}'
    print(formatted_text)
    try:
        os.makedirs(LOGS_FOLDER, exist_ok=True)
        log_file_path = os.path.join(LOGS_FOLDER, 'bot.log')
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(formatted_text + '\n')
    except Exception:
        pass

def log_info_message(message: str) -> None:
    write_log_message('INFO', message)

def log_warning_message(message: str) -> None:
    write_log_message('WARNING', message)

def log_error_message(message: str) -> None:
    write_log_message('ERROR', message)

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ СОЗДАНИЯ КЛАВИАТУР
# ═══════════════════════════════════════════════════════════════════════════════════════

def create_main_menu_keyboard_for_user(user_id: int) -> ReplyKeyboardMarkup:
    row_one = KeyboardButtonRow(buttons=[
        KeyboardButton('📞 Номер'),
        KeyboardButton('📧 Email')
    ])
    row_two = KeyboardButtonRow(buttons=[
        KeyboardButton('🌐 IP'),
        KeyboardButton('🔍 VK')
    ])
    row_three = KeyboardButtonRow(buttons=[
        KeyboardButton('💻 MAC'),
        KeyboardButton('🆔 По ID')
    ])
    row_four = KeyboardButtonRow(buttons=[
        KeyboardButton('🤖 Зеркало'),
        KeyboardButton('🔗 Рефералы')
    ])
    row_five = KeyboardButtonRow(buttons=[
        KeyboardButton('⭐ Подписка'),
        KeyboardButton('ℹ️ О боте')
    ])
    
    all_rows = [row_one, row_two, row_three, row_four, row_five]
    
    if is_user_admin(user_id):
        admin_row = KeyboardButtonRow(buttons=[
            KeyboardButton('🛡 Админ панель')
        ])
        all_rows.append(admin_row)
    
    keyboard = ReplyKeyboardMarkup(
        rows=all_rows,
        resize=True,
        placeholder='Выберите действие из меню...'
    )
    return keyboard

def create_cancel_keyboard_button() -> ReplyKeyboardMarkup:
    row = KeyboardButtonRow(buttons=[
        KeyboardButton('🔙 Отмена')
    ])
    keyboard = ReplyKeyboardMarkup(rows=[row], resize=True)
    return keyboard

def create_back_to_menu_keyboard_button() -> ReplyKeyboardMarkup:
    row = KeyboardButtonRow(buttons=[
        KeyboardButton('🔙 В меню')
    ])
    keyboard = ReplyKeyboardMarkup(rows=[row], resize=True)
    return keyboard

def create_admin_panel_keyboard_for_user(user_id: int) -> ReplyKeyboardMarkup:
    admin_level = get_admin_level(user_id)
    all_rows = []
    
    row_one = KeyboardButtonRow(buttons=[
        KeyboardButton('📊 Статистика'),
        KeyboardButton('👥 Пользователи')
    ])
    all_rows.append(row_one)
    
    if ADMIN_PERMISSIONS.get(admin_level, {}).get('can_ban', False):
        row_two = KeyboardButtonRow(buttons=[
            KeyboardButton('🔨 Бан'),
            KeyboardButton('✅ Разбан')
        ])
        all_rows.append(row_two)
    
    if ADMIN_PERMISSIONS.get(admin_level, {}).get('can_mute', False):
        row_three = KeyboardButtonRow(buttons=[
            KeyboardButton('🔇 Мут'),
            KeyboardButton('🔊 Размут')
        ])
        all_rows.append(row_three)
    
    if admin_level >= 4:
        row_four = KeyboardButtonRow(buttons=[
            KeyboardButton('📋 Админы'),
            KeyboardButton('⬆ Повысить')
        ])
        all_rows.append(row_four)
        
        row_five = KeyboardButtonRow(buttons=[
            KeyboardButton('⬇ Понизить'),
            KeyboardButton('🎁 Подписка+')
        ])
        all_rows.append(row_five)
    
    if ADMIN_PERMISSIONS.get(admin_level, {}).get('can_broadcast', False):
        row_six = KeyboardButtonRow(buttons=[
            KeyboardButton('📢 Рассылка'),
            KeyboardButton('🔄 Перезапуск')
        ])
        all_rows.append(row_six)
    
    row_seven = KeyboardButtonRow(buttons=[
        KeyboardButton('⚡ Белый список'),
        KeyboardButton('🔙 В меню')
    ])
    all_rows.append(row_seven)
    
    keyboard = ReplyKeyboardMarkup(
        rows=all_rows,
        resize=True,
        placeholder='Админ-панель...'
    )
    return keyboard

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ФОРМАТИРОВАНИЯ
# ═══════════════════════════════════════════════════════════════════════════════════════

def format_phone_number_for_display(phone: str) -> str:
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 11 and cleaned.startswith('7'):
        return f"+7 ({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:9]}-{cleaned[9:11]}"
    return phone

def get_country_flag_emoji(country: str) -> str:
    flags = {
        'Россия': '🇷🇺',
        'Российская Федерация': '🇷🇺',
        'Украина': '🇺🇦',
        'Беларусь': '🇧🇾',
        'Казахстан': '🇰🇿',
        'США': '🇺🇸',
        'Германия': '🇩🇪',
        'Франция': '🇫🇷'
    }
    return flags.get(country, '🌍')

def format_phone_lookup_result(phone: str, htmlweb_data: Dict[str, Any], bot_data: Optional[str]) -> str:
    formatted_phone = format_phone_number_for_display(phone)
    current_date = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    operator = htmlweb_data.get('operator', 'Неизвестно')
    region = htmlweb_data.get('region', 'Неизвестно')
    city = htmlweb_data.get('city', 'Неизвестно')
    country = htmlweb_data.get('country', 'Неизвестно')
    brand = htmlweb_data.get('brand', 'Неизвестно')
    flag_emoji = get_country_flag_emoji(country)
    
    result_text = f"""<b>🕵️ РЕЗУЛЬТАТ</b>
<b>📅 {current_date}</b>

<b>📱 {formatted_phone}</b>
<b>📡 {operator} | {region} | {city}</b>
"""
    
    if bot_data:
        result_text += f"""<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
{bot_data}
"""
    
    return result_text

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ API ЗАПРОСОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

async def lookup_phone_htmlweb(phone_number: str) -> Dict[str, Any]:
    cleaned_number = re.sub(r'\D', '', phone_number)
    request_url = HTMLWEB_API_URL.format(number=cleaned_number)
    
    log_info_message(f'[HTMLWEB] Запрос: {cleaned_number}')
    
    try:
        async with ClientSession() as session:
            async with session.get(request_url, timeout=ClientTimeout(total=10)) as response:
                response_data = await response.json()
                
                result = {
                    'country': response_data.get('fullname', 'Неизвестно'),
                    'region': response_data.get('region', {}).get('name', 'Неизвестно'),
                    'city': response_data.get('0', {}).get('name', 'Неизвестно'),
                    'operator': response_data.get('0', {}).get('oper', 'Неизвестно'),
                    'brand': response_data.get('0', {}).get('oper_brand', 'Неизвестно'),
                    'range': response_data.get('0', {}).get('def', 'Неизвестно'),
                    'mobile': response_data.get('0', {}).get('mobile', False),
                    'timezone': response_data.get('tz', 'Неизвестно'),
                    'postal': response_data.get('0', {}).get('post', 'Неизвестно'),
                }
                
                log_info_message(f'[HTMLWEB] Город: {result["city"]}, Оператор: {result["operator"]}')
                return result
                
    except Exception as error:
        log_error_message(f'[HTMLWEB] Ошибка: {error}')
        return {
            'country': 'Неизвестно',
            'region': 'Неизвестно',
            'city': 'Неизвестно',
            'operator': 'Неизвестно',
            'brand': 'Неизвестно',
            'range': 'Неизвестно',
            'mobile': False,
            'timezone': 'Неизвестно',
            'postal': 'Неизвестно',
        }

async def search_with_telegram_bot(phone_number: str) -> Optional[str]:
    log_info_message(f'[SEARCH BOT] Пробив: {phone_number}')
    
    telegram_client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    result_text = None
    
    try:
        await telegram_client.start()
        
        try:
            async for message in telegram_client.iter_messages(SEARCH_BOT_USERNAME, limit=10):
                if message.out:
                    await message.delete()
        except Exception:
            pass
        
        await telegram_client.send_message(SEARCH_BOT_USERNAME, '/start')
        await asyncio.sleep(1.5)
        
        messages = await telegram_client.get_messages(SEARCH_BOT_USERNAME, limit=1)
        if messages and messages[0].buttons:
            await messages[0].click(0, 0)
            await asyncio.sleep(1)
            
            submenu_messages = await telegram_client.get_messages(SEARCH_BOT_USERNAME, limit=1)
            if submenu_messages and submenu_messages[0].buttons:
                await submenu_messages[0].click(0, 0)
                await asyncio.sleep(0.5)
                
                await telegram_client.send_message(SEARCH_BOT_USERNAME, phone_number)
                await asyncio.sleep(4)
                
                result_messages = await telegram_client.get_messages(SEARCH_BOT_USERNAME, limit=5)
                for msg in result_messages:
                    if msg.text and '📱' in msg.text:
                        result_text = msg.text
                        result_text = result_text.replace('by ****@sjgdfj0ghjdhjjegtjjebot', '')
                        result_text = result_text.replace('by @sjgdfj0ghjdhjjegtjjebot', '')
                        result_text = result_text.replace('****', '')
                        break
        
        return result_text
        
    except Exception as error:
        log_error_message(f'[SEARCH BOT] Ошибка: {error}')
        return None
        
    finally:
        try:
            await telegram_client.disconnect()
        except Exception:
            pass

async def search_vk_profiles_api(query: str) -> List[Dict[str, Any]]:
    request_url = VK_API_URL.format(token=VK_ACCESS_TOKEN, query=query)
    
    try:
        async with ClientSession() as session:
            async with session.get(request_url, timeout=ClientTimeout(total=10)) as response:
                data = await response.json()
                if 'response' in data:
                    return data['response']
                return []
    except Exception as error:
        log_error_message(f'[VK] Ошибка: {error}')
        return []

async def check_leaks_leakcheck_api(query: str) -> List[Dict[str, Any]]:
    request_url = LEAKCHECK_API_URL.format(key=LEAKCHECK_API_KEY, query=query)
    
    try:
        async with ClientSession() as session:
            async with session.get(request_url, timeout=ClientTimeout(total=15)) as response:
                data = await response.json()
                if data.get('success') and data.get('result'):
                    return data['result']
                return []
    except Exception as error:
        log_error_message(f'[LEAKCHECK] Ошибка: {error}')
        return []

async def lookup_ip_address_api(ip_address: str) -> Dict[str, Any]:
    request_url = IPINFO_API_URL.format(ip=ip_address, key=IPINFO_API_KEY)
    
    try:
        async with ClientSession() as session:
            async with session.get(request_url, timeout=ClientTimeout(total=10)) as response:
                return await response.json()
    except Exception as error:
        log_error_message(f'[IPINFO] Ошибка: {error}')
        return {}

async def lookup_mac_address_api(mac_address: str) -> Optional[str]:
    request_url = MACVENDORS_API_URL.format(mac=mac_address)
    
    try:
        async with ClientSession() as session:
            async with session.get(request_url, timeout=ClientTimeout(total=10)) as response:
                return await response.text()
    except Exception as error:
        log_error_message(f'[MAC] Ошибка: {error}')
        return None

async def search_telegram_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    telegram_client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    
    try:
        await telegram_client.start()
        entity = await telegram_client.get_entity(int(user_id))
        
        result = {
            'first_name': entity.first_name or '',
            'last_name': entity.last_name or '',
            'username': entity.username or '',
            'phone': getattr(entity, 'phone', None)
        }
        return result
        
    except Exception as error:
        log_error_message(f'[SEARCH ID] Ошибка: {error}')
        return None
        
    finally:
        try:
            await telegram_client.disconnect()
        except Exception:
            pass

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ ЗЕРКАЛ
# ═══════════════════════════════════════════════════════════════════════════════════════

def get_mirrors_list_from_file() -> Dict[str, Any]:
    if not os.path.exists(MIRRORS_FILE):
        return {}
    try:
        with open(MIRRORS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return {}

def save_mirror_info_to_file(bot_token: str, bot_name: str, bot_username: str) -> None:
    os.makedirs(MIRRORS_FOLDER, exist_ok=True)
    mirrors = get_mirrors_list_from_file()
    mirrors[bot_token] = {
        'name': bot_name,
        'username': bot_username,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(MIRRORS_FILE, 'w', encoding='utf-8') as file:
        json.dump(mirrors, file, ensure_ascii=False, indent=4)

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ БЕЛОГО СПИСКА
# ═══════════════════════════════════════════════════════════════════════════════════════

def load_whitelist_from_file() -> Dict[str, Any]:
    if not os.path.exists(WHITELIST_FILE):
        return {}
    try:
        with open(WHITELIST_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return {}

def save_to_whitelist_file(phone: str, data: Dict[str, Any]) -> None:
    whitelist = load_whitelist_from_file()
    whitelist[phone] = data
    os.makedirs(os.path.dirname(WHITELIST_FILE), exist_ok=True)
    with open(WHITELIST_FILE, 'w', encoding='utf-8') as file:
        json.dump(whitelist, file, ensure_ascii=False, indent=4)

def check_phone_in_whitelist(phone: str) -> bool:
    cleaned = re.sub(r'\D', '', phone)
    whitelist = load_whitelist_from_file()
    return cleaned in whitelist

# ═══════════════════════════════════════════════════════════════════════════════════════
# СПИСОК КНОПОК КЛАВИАТУРЫ
# ═══════════════════════════════════════════════════════════════════════════════════════

KEYBOARD_BUTTONS: List[str] = [
    '📞 Номер',
    '📧 Email',
    '🌐 IP',
    '🔍 VK',
    '💻 MAC',
    '🆔 По ID',
    '🤖 Зеркало',
    '🔗 Рефералы',
    '⭐ Подписка',
    'ℹ️ О боте',
    '🛡 Админ панель',
    '🔙 Отмена',
    '🔙 В меню',
    '✅ Проверить подписку',
    '📊 Статистика',
    '👥 Пользователи',
    '🔨 Бан',
    '🔇 Мут',
    '✅ Разбан',
    '🔊 Размут',
    '📋 Админы',
    '⬆ Повысить',
    '⬇ Понизить',
    '🎁 Подписка+',
    '📢 Рассылка',
    '🔄 Перезапуск',
    '⚡ Белый список'
]

# ═══════════════════════════════════════════════════════════════════════════════════════
# ЗАГРУЗКА ДАННЫХ ПРИ СТАРТЕ
# ═══════════════════════════════════════════════════════════════════════════════════════

load_admins_from_file()
load_bans_from_file()
load_mutes_from_file()

log_info_message(f'Загружено администраторов: {len(admins)}')
log_info_message(f'Забанено пользователей: {len(banned_users)}')
log_info_message(f'Замьючено пользователей: {len(muted_users)}')

# ═══════════════════════════════════════════════════════════════════════════════════════
# СОЗДАНИЕ И ЗАПУСК ТЕЛЕГРАМ БОТА
# ═══════════════════════════════════════════════════════════════════════════════════════

log_info_message('Создаю клиент Telegram бота...')

telegram_bot = TelegramClient(
    'dix_telegram_bot',
    API_ID,
    API_HASH,
    device_model='Samsung Galaxy S24 Ultra',
    system_version='Android 14',
    app_version='11.5.3',
    lang_code='ru',
    system_lang_code='ru-RU'
)

try:
    telegram_bot.start(bot_token=BOT_TOKEN)
    log_info_message('Бот успешно запущен')
except FloodWaitError as error:
    log_warning_message(f'FloodWait {error.seconds} секунд. Ожидание...')
    time.sleep(error.seconds + 5)
    telegram_bot.start(bot_token=BOT_TOKEN)

# ═══════════════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИК КОМАНДЫ /start
# ═══════════════════════════════════════════════════════════════════════════════════════

@telegram_bot.on(events.NewMessage(pattern='/start'))
async def handle_start_command(event):
    user_id = event.sender_id
    user_first_name = event.sender.first_name
    user_username = event.sender.username
    
    # Проверка на флуд
    if check_user_flood(user_id):
        await event.respond(
            '<b>🔇 ФЛУД!</b>\n\n'
            '<b>Вы замьючены на 10 минут за превышение лимита сообщений.</b>',
            parse_mode='html'
        )
        return
    
    # Проверка на бан
    if is_user_banned(user_id):
        ban_info = banned_users[user_id]
        await event.respond(
            f'<b>⛔ ВЫ ЗАБЛОКИРОВАНЫ</b>\n\n'
            f'<b>Причина:</b> {ban_info["reason"]}\n'
            f'<b>Дата:</b> {ban_info["banned_at"]}\n\n'
            f'<i>Обратитесь к администратору: {OWNER_USERNAME}</i>',
            parse_mode='html'
        )
        return
    
    # Проверка на мут
    if is_user_muted(user_id):
        mute_info = muted_users[user_id]
        await event.respond(
            f'<b>🔇 ВЫ ЗАМЬЮЧЕНЫ</b>\n\n'
            f'<b>Причина:</b> {mute_info["reason"]}\n'
            f'<b>До:</b> {mute_info["mute_until"]}\n\n'
            f'<i>Ожидайте окончания мута</i>',
            parse_mode='html'
        )
        return
    
    # Сбрасываем состояние пользователя
    user_states[user_id] = None
    
    # Обработка реферальной ссылки
    message_text = event.text
    if 'ref' in message_text:
        try:
            referrer_id = int(message_text.split('ref')[1].split()[0])
            if referrer_id != user_id and user_id not in user_referrals:
                user_referrals[user_id] = str(referrer_id)
                if referrer_id in user_limits:
                    user_limits[referrer_id]['count'] = max(0, user_limits[referrer_id].get('count', 0) - 1)
                try:
                    await telegram_bot.send_message(
                        referrer_id,
                        f'<b>🎁 НОВЫЙ РЕФЕРАЛ!</b>\n\n'
                        f'<b>Пользователь:</b> {user_first_name}\n'
                        f'<b>Бонус:</b> +{REFERRAL_BONUS} запрос сегодня',
                        parse_mode='html'
                    )
                except Exception:
                    pass
        except Exception:
            pass
    
    # Приветственное сообщение
    welcome_text = f"""<b>🕵️ Прoект #Амнезия</b>

<b>Сервис прoверки публичнoй инфoрмации</b>
<b>и цифрoвых следoв пoльзoвателя</b>

<b>Сoздатель: @kapolam</b>
<b>Владелец: @kepber</b>

<b>👇 Выберите действие:</b>"""
    
    main_menu_keyboard = create_main_menu_keyboard_for_user(user_id)
    await event.respond(welcome_text, buttons=main_menu_keyboard, parse_mode='html')

# ═══════════════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИК НАЖАТИЙ НА КНОПКИ КЛАВИАТУРЫ
# ═══════════════════════════════════════════════════════════════════════════════════════

@telegram_bot.on(events.NewMessage(func=lambda e: e.is_private and e.text in KEYBOARD_BUTTONS))
async def handle_keyboard_buttons(event):
    user_id = event.sender_id
    button_text = event.text.strip()
    
    # Проверка на флуд
    if check_user_flood(user_id):
        return
    
    # Проверка на бан
    if is_user_banned(user_id):
        return
    
    # Проверка на мут
    if is_user_muted(user_id):
        return
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА КНОПОК ГЛАВНОГО МЕНЮ
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    if button_text == '📞 Номер':
        user_states[user_id] = 'waiting_phone'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>📞 Введите номер телефона:</b>\n\n'
            '<i>Пример: +79999999999</i>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '📧 Email':
        user_states[user_id] = 'waiting_email'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>📧 Введите email адрес:</b>\n\n'
            '<i>Пример: example@gmail.com</i>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🌐 IP':
        user_states[user_id] = 'waiting_ip'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🌐 Введите IP адрес:</b>\n\n'
            '<i>Пример: 8.8.8.8</i>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🔍 VK':
        user_states[user_id] = 'waiting_vk'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🔍 Введите ID или имя для поиска VK:</b>\n\n'
            '<i>Пример: 1 или Иван Иванов</i>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '💻 MAC':
        user_states[user_id] = 'waiting_mac'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>💻 Введите MAC адрес:</b>\n\n'
            '<i>Пример: 00:1A:2B:3C:4D:5E</i>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🆔 По ID':
        user_states[user_id] = 'waiting_tg_id'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🆔 Введите Telegram ID:</b>\n\n'
            '<i>Пример: 5817293461</i>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🤖 Зеркало':
        user_states[user_id] = 'waiting_mirror_token'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🤖 СОЗДАНИЕ ЗЕРКАЛА</b>\n\n'
            '<b>Инструкция:</b>\n'
            '1. Зайдите в @BotFather\n'
            '2. Отправьте /newbot\n'
            '3. Придумайте имя и username\n'
            '4. Скопируйте токен\n\n'
            '<b>⬇️ Отправьте токен:</b>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🔗 Рефералы':
        referral_link = generate_referral_link_for_user(user_id)
        referral_count = sum(1 for value in user_referrals.values() if value == str(user_id))
        await event.respond(
            f'<b>🔗 РЕФЕРАЛЬНАЯ СИСТЕМА</b>\n\n'
            f'<b>Ваша ссылка:</b>\n'
            f'<code>{referral_link}</code>\n\n'
            f'<b>Перешло по ссылке:</b> {referral_count}\n'
            f'<b>Бонус за каждого:</b> +{REFERRAL_BONUS} запрос\n\n'
            f'<i>Отправьте ссылку другу. Когда он зайдёт — вы получите +1 запрос.</i>',
            parse_mode='html'
        )
    
    elif button_text == '⭐ Подписка':
        if check_user_subscription(user_id):
            await event.respond(
                '<b>✅ ПОДПИСКА АКТИВНА</b>\n\n'
                '<b>У вас безлимитные запросы.</b>',
                parse_mode='html'
            )
        else:
            subscription_check_keyboard = ReplyKeyboardMarkup(
                rows=[[KeyboardButtonRow(buttons=[KeyboardButton('✅ Проверить подписку')])]],
                resize=True
            )
            await event.respond(
                f'<b>⭐ ПОДПИСКА</b>\n\n'
                f'<b>Подпишитесь на канал:</b> {SUBSCRIPTION_CHANNEL}\n\n'
                f'<b>После подписки:</b>\n'
                f'• Безлимитные запросы\n'
                f'• Приоритетная обработка\n\n'
                f'<b>Затем нажмите кнопку ниже для проверки.</b>',
                buttons=subscription_check_keyboard,
                parse_mode='html'
            )
    
    elif button_text == '✅ Проверить подписку':
        try:
            await telegram_bot(GetParticipantRequest(SUBSCRIPTION_CHANNEL, user_id))
            user_subscriptions[user_id] = True
            main_menu_keyboard = create_main_menu_keyboard_for_user(user_id)
            await event.respond(
                '<b>✅ ПОДПИСКА АКТИВИРОВАНА!</b>\n\n'
                '<b>Теперь у вас безлимитные запросы!</b>',
                buttons=main_menu_keyboard,
                parse_mode='html'
            )
        except Exception:
            await event.respond(
                f'<b>❌ ВЫ НЕ ПОДПИСАНЫ</b>\n\n'
                f'<b>Подпишитесь на канал:</b> {SUBSCRIPTION_CHANNEL}\n'
                f'<i>И нажмите кнопку проверки снова.</i>',
                parse_mode='html'
            )
    
    elif button_text == 'ℹ️ О боте':
        await event.respond(
            '<b>🕵️ DIX OSINT</b>\n\n'
            '📞 Номер\n'
            '📧 Email\n'
            '🌐 IP\n'
            '🔍 VK\n'
            '💻 MAC\n'
            '🆔 По ID\n'
            '🤖 Зеркала',
            parse_mode='html'
        )
    
    elif button_text == '🔙 Отмена':
        user_states[user_id] = None
        main_menu_keyboard = create_main_menu_keyboard_for_user(user_id)
        await event.respond(
            '<b>❌ Действие отменено.</b>',
            buttons=main_menu_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🔙 В меню':
        user_states[user_id] = None
        main_menu_keyboard = create_main_menu_keyboard_for_user(user_id)
        await event.respond(
            '<b>🕵️ Прoект #Амнезия</b>\n\n'
            '<b>👇 Выберите действие:</b>',
            buttons=main_menu_keyboard,
            parse_mode='html'
        )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА КНОПОК АДМИН-ПАНЕЛИ
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif button_text == '🛡 Админ панель':
        if not is_user_admin(user_id):
            await event.respond('<b>⛔ Доступ запрещён.</b>', parse_mode='html')
            return
        
        admin_level = get_admin_level(user_id)
        admin_level_name = ADMIN_LEVEL_NAMES.get(admin_level, 'Неизвестно')
        admin_daily_limit = get_admin_daily_limit(user_id)
        admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
        
        await event.respond(
            f'<b>🛡 АДМИН ПАНЕЛЬ</b>\n\n'
            f'<b>Ваш уровень:</b> {admin_level} — {admin_level_name}\n'
            f'<b>Лимит запросов:</b> {admin_daily_limit} в день\n'
            f'<b>Всего админов:</b> {len(admins)}\n'
            f'<b>Забанено:</b> {len(banned_users)}\n'
            f'<b>Замьючено:</b> {len(muted_users)}\n\n'
            f'<b>👇 Выберите действие:</b>',
            buttons=admin_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '📊 Статистика':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if not ADMIN_PERMISSIONS.get(admin_level, {}).get('can_view_stats', False):
            await event.respond('<b>⛔ Недостаточно прав.</b>', parse_mode='html')
            return
        
        await event.respond(
            f'<b>📊 СТАТИСТИКА БОТА</b>\n\n'
            f'<b>Пользователей:</b> {len(user_states)}\n'
            f'<b>Админов:</b> {len(admins)}\n'
            f'<b>Забанено:</b> {len(banned_users)}\n'
            f'<b>Замьючено:</b> {len(muted_users)}\n'
            f'<b>С подпиской:</b> {len(user_subscriptions)}',
            parse_mode='html'
        )
    
    elif button_text == '👥 Пользователи':
        if not is_user_admin(user_id):
            return
        
        users_list = list(user_states.keys())
        if not users_list:
            await event.respond('<b>👥 Нет активных пользователей.</b>', parse_mode='html')
            return
        
        users_text = f'<b>👥 ПОЛЬЗОВАТЕЛИ</b>\n\n<b>Всего:</b> {len(users_list)}\n\n'
        for uid in users_list[:20]:
            ban_mark = ' 🚫' if is_user_banned(uid) else ''
            mute_mark = ' 🔇' if is_user_muted(uid) else ''
            admin_mark = f' 👑{get_admin_level(uid)}' if is_user_admin(uid) else ''
            users_text += f'• <code>{uid}</code>{ban_mark}{mute_mark}{admin_mark}\n'
        
        await event.respond(users_text, parse_mode='html')
    
    elif button_text == '🔨 Бан':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if not ADMIN_PERMISSIONS.get(admin_level, {}).get('can_ban', False):
            await event.respond('<b>⛔ Нет прав на бан.</b>', parse_mode='html')
            return
        
        user_states[user_id] = 'waiting_ban'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🔨 БАН ПОЛЬЗОВАТЕЛЯ</b>\n\n'
            '<b>Отправьте ID и причину:</b>\n'
            '<code>123456789 причина бана</code>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🔇 Мут':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if not ADMIN_PERMISSIONS.get(admin_level, {}).get('can_mute', False):
            await event.respond('<b>⛔ Нет прав на мут.</b>', parse_mode='html')
            return
        
        max_mute_minutes = ADMIN_PERMISSIONS.get(admin_level, {}).get('max_mute_minutes', 0)
        user_states[user_id] = 'waiting_mute'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            f'<b>🔇 МУТ ПОЛЬЗОВАТЕЛЯ</b>\n\n'
            f'<b>Максимум:</b> {max_mute_minutes} минут\n\n'
            f'<b>Отправьте ID, минуты и причину:</b>\n'
            f'<code>123456789 60 причина мута</code>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '✅ Разбан':
        if not is_user_admin(user_id):
            return
        
        user_states[user_id] = 'waiting_unban'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>✅ РАЗБАН</b>\n\n'
            '<b>Отправьте ID пользователя:</b>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🔊 Размут':
        if not is_user_admin(user_id):
            return
        
        user_states[user_id] = 'waiting_unmute'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🔊 РАЗМУТ</b>\n\n'
            '<b>Отправьте ID пользователя:</b>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '📋 Админы':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if admin_level < 4:
            await event.respond('<b>⛔ Недостаточно прав.</b>', parse_mode='html')
            return
        
        if not admins:
            await event.respond('<b>📋 Список админов пуст.</b>', parse_mode='html')
            return
        
        admins_text = f'<b>📋 АДМИНИСТРАТОРЫ ({len(admins)})</b>\n\n'
        for admin_id, admin_info in admins.items():
            level = admin_info.get('level', 0)
            level_name = ADMIN_LEVEL_NAMES.get(level, 'Неизвестно')
            added_by = admin_info.get('added_by', '?')
            added_date = admin_info.get('added_date', '?')
            owner_mark = ' 👑' if level == 7 else ''
            admins_text += f'• <code>{admin_id}</code> — {level_name}{owner_mark}\n'
            admins_text += f'  Добавлен: {added_by}, Дата: {added_date}\n'
        
        await event.respond(admins_text, parse_mode='html')
    
    elif button_text == '⬆ Повысить':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        max_promote = ADMIN_PERMISSIONS.get(admin_level, {}).get('can_promote_to', 0)
        
        if max_promote <= 0:
            await event.respond('<b>⛔ Нет прав на повышение.</b>', parse_mode='html')
            return
        
        user_states[user_id] = 'waiting_promote'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            f'<b>⬆ ПОВЫШЕНИЕ</b>\n\n'
            f'<b>Вы можете повысить до уровня:</b> {max_promote}\n\n'
            f'<b>Отправьте ID и уровень:</b>\n'
            f'<code>123456789 3</code>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '⬇ Понизить':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if admin_level < 4:
            await event.respond('<b>⛔ Недостаточно прав.</b>', parse_mode='html')
            return
        
        user_states[user_id] = 'waiting_demote'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>⬇ ПОНИЖЕНИЕ</b>\n\n'
            '<b>Отправьте ID и новый уровень:</b>\n'
            '<code>123456789 1</code>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🎁 Подписка+':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if admin_level < 4:
            await event.respond('<b>⛔ Недостаточно прав.</b>', parse_mode='html')
            return
        
        user_states[user_id] = 'waiting_gift_sub'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>🎁 ПОДАРИТЬ ПОДПИСКУ</b>\n\n'
            '<b>Отправьте ID пользователя:</b>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '📢 Рассылка':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if not ADMIN_PERMISSIONS.get(admin_level, {}).get('can_broadcast', False):
            await event.respond('<b>⛔ Недостаточно прав.</b>', parse_mode='html')
            return
        
        user_states[user_id] = 'waiting_broadcast'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>📢 РАССЫЛКА</b>\n\n'
            '<b>Отправьте сообщение для рассылки всем пользователям:</b>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )
    
    elif button_text == '🔄 Перезапуск':
        if not is_user_admin(user_id):
            return
        
        admin_level = get_admin_level(user_id)
        if admin_level < 6:
            await event.respond('<b>⛔ Недостаточно прав.</b>', parse_mode='html')
            return
        
        await event.respond('<b>🔄 Перезапускаю бота...</b>', parse_mode='html')
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    elif button_text == '⚡ Белый список':
        if not is_user_admin(user_id):
            return
        
        user_states[user_id] = 'waiting_whitelist'
        cancel_keyboard = create_cancel_keyboard_button()
        await event.respond(
            '<b>⚡ ДОБАВЛЕНИЕ В БЕЛЫЙ СПИСОК</b>\n\n'
            '<b>Формат:</b>\n'
            'Номер: +79999999999\n'
            'ФИО: Иванов Иван Иванович\n'
            'Адрес: г. Москва\n\n'
            '<b>⬇️ Отправьте данные:</b>',
            buttons=cancel_keyboard,
            parse_mode='html'
        )

# ═══════════════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИК ВХОДЯЩИХ СООБЩЕНИЙ
# ═══════════════════════════════════════════════════════════════════════════════════════

@telegram_bot.on(events.NewMessage(func=lambda e: not e.text.startswith('/') and e.is_private and e.text not in KEYBOARD_BUTTONS))
async def handle_incoming_messages(event):
    user_id = event.sender_id
    current_state = user_states.get(user_id)
    message_text = event.text.strip()
    
    if not current_state:
        return
    
    if is_user_banned(user_id):
        return
    
    if is_user_muted(user_id):
        return
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА ПРОБИВА НОМЕРА ТЕЛЕФОНА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    if current_state == 'waiting_phone':
        cleaned_number = re.sub(r'\D', '', message_text)
        
        if len(cleaned_number) < 10:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат номера.</b>\n\n'
                '<i>Попробуйте ещё раз или нажмите Отмена.</i>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
            return
        
        if check_phone_in_whitelist(cleaned_number):
            back_keyboard = create_back_to_menu_keyboard_button()
            await event.respond(
                '<b>⚡ ДАННЫЕ НАХОДЯТСЯ В БЕЛОМ СПИСКЕ</b>\n\n'
                '<i>Подробнее у тех.поддержки.</i>',
                buttons=back_keyboard,
                parse_mode='html'
            )
            return
        
        if not can_user_make_request(user_id) and user_id != OWNER_ID:
            current_count = get_user_requests_count_today(user_id)
            limit = get_user_daily_limit(user_id)
            await event.respond(
                f'<b>❌ ДОСТИГНУТ ЛИМИТ ЗАПРОСОВ</b>\n\n'
                f'<b>Использовано:</b> {current_count}/{limit}\n\n'
                f'<b>Чтобы получить больше:</b>\n'
                f'• Подпишитесь на {SUBSCRIPTION_CHANNEL}\n'
                f'• Пригласите друга по реферальной ссылке\n'
                f'• Станьте администратором',
                parse_mode='html'
            )
            return
        
        increment_user_requests_count(user_id)
        
        status_message = await event.respond(
            '<b>🔍 ЗАПУСК ПОИСКА...</b>\n'
            '<i>Ожидайте, поиск идёт...</i>',
            parse_mode='html'
        )
        
        await status_message.edit(
            '<b>⏳ [1/2] Город и оператор...</b>\n'
            '<i>Ожидайте, поиск идёт...</i>',
            parse_mode='html'
        )
        htmlweb_data = await lookup_phone_htmlweb(cleaned_number)
        
        await status_message.edit(
            '<b>⏳ [2/2] Телефонные книги и соцсети...</b>\n'
            '<i>Ожидайте, поиск идёт...</i>',
            parse_mode='html'
        )
        bot_data = await search_with_telegram_bot(cleaned_number)
        
        result = format_phone_lookup_result(message_text, htmlweb_data, bot_data)
        
        user_states[user_id] = None
        
        back_keyboard = create_back_to_menu_keyboard_button()
        try:
            await status_message.edit(result, buttons=back_keyboard, parse_mode='html')
        except Exception:
            await status_message.edit(
                '<b>✅ Готово!</b>\n\n'
                '<b>Результат получен.</b>',
                buttons=back_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА EMAIL
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_email':
        if '@' not in message_text:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат email.</b>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
            return
        
        status_message = await event.respond(
            '<b>⏳ Проверка email...</b>',
            parse_mode='html'
        )
        
        await status_message.edit(
            f'<b>📧 РЕЗУЛЬТАТ</b>\n\n'
            f'<b>Email:</b> <code>{message_text}</code>\n'
            f'<b>✅ Проверено</b>',
            buttons=create_back_to_menu_keyboard_button(),
            parse_mode='html'
        )
        
        user_states[user_id] = None
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА IP
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_ip':
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', message_text):
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат IP.</b>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
            return
        
        status_message = await event.respond(
            '<b>⏳ Поиск IP...</b>',
            parse_mode='html'
        )
        
        ip_data = await lookup_ip_address_api(message_text)
        
        await status_message.edit(
            f'<b>🌐 РЕЗУЛЬТАТ</b>\n\n'
            f'<b>IP:</b> <code>{message_text}</code>\n'
            f'<b>Город:</b> {ip_data.get("city", "Неизвестно")}\n'
            f'<b>Регион:</b> {ip_data.get("region", "Неизвестно")}\n'
            f'<b>Страна:</b> {ip_data.get("country", "Неизвестно")}\n'
            f'<b>Провайдер:</b> {ip_data.get("org", "Неизвестно")}',
            buttons=create_back_to_menu_keyboard_button(),
            parse_mode='html'
        )
        
        user_states[user_id] = None
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА VK
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_vk':
        status_message = await event.respond(
            '<b>⏳ Поиск VK...</b>',
            parse_mode='html'
        )
        
        profiles = await search_vk_profiles_api(message_text)
        
        if profiles:
            result_text = f'<b>🔍 НАЙДЕНО VK ПРОФИЛЕЙ:</b> {len(profiles)}\n\n'
            for profile in profiles[:5]:
                first_name = profile.get('first_name', '')
                last_name = profile.get('last_name', '')
                user_identifier = profile.get('id', '')
                result_text += f'• <a href="https://vk.com/id{user_identifier}">{first_name} {last_name}</a>\n'
        else:
            result_text = '<b>❌ VK профили не найдены.</b>'
        
        await status_message.edit(
            result_text,
            buttons=create_back_to_menu_keyboard_button(),
            parse_mode='html'
        )
        
        user_states[user_id] = None
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА MAC
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_mac':
        status_message = await event.respond(
            '<b>⏳ Определение MAC...</b>',
            parse_mode='html'
        )
        
        vendor = await lookup_mac_address_api(message_text)
        
        await status_message.edit(
            f'<b>💻 РЕЗУЛЬТАТ</b>\n\n'
            f'<b>MAC:</b> <code>{message_text}</code>\n'
            f'<b>Производитель:</b> {vendor if vendor else "Не найден"}',
            buttons=create_back_to_menu_keyboard_button(),
            parse_mode='html'
        )
        
        user_states[user_id] = None
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА TELEGRAM ID
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_tg_id':
        status_message = await event.respond(
            '<b>⏳ Поиск по Telegram ID...</b>',
            parse_mode='html'
        )
        
        user_data = await search_telegram_user_by_id(message_text)
        
        if user_data:
            first_name = user_data.get('first_name', 'Не указано')
            last_name = user_data.get('last_name', 'Не указана')
            username = user_data.get('username', '')
            phone = user_data.get('phone', 'Скрыт')
            
            result_text = f'''<b>🆔 РЕЗУЛЬТАТ ПОИСКА ПО ID</b>

<b>🆔 ID:</b> <code>{message_text}</code>
<b>👤 Имя:</b> {first_name}
<b>👤 Фамилия:</b> {last_name}
<b>📛 Username:</b> @{username if username else 'Не указан'}
<b>📱 Телефон:</b> {phone if phone else 'Скрыт'}'''
        else:
            result_text = '<b>❌ Пользователь не найден.</b>'
        
        await status_message.edit(
            result_text,
            buttons=create_back_to_menu_keyboard_button(),
            parse_mode='html'
        )
        
        user_states[user_id] = None
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА ТОКЕНА ЗЕРКАЛА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_mirror_token':
        token = message_text.strip()
        
        if ':' not in token:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат токена.</b>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
            return
        
        status_message = await event.respond(
            '<b>⏳ Проверяю токен...</b>',
            parse_mode='html'
        )
        
        try:
            test_client = TelegramClient('mirror_test', API_ID, API_HASH)
            await test_client.start(bot_token=token)
            bot_info = await test_client.get_me()
            bot_name = bot_info.first_name
            bot_username = bot_info.username
            
            save_mirror_info_to_file(token, bot_name, bot_username)
            
            await test_client.disconnect()
            
            user_states[user_id] = None
            back_keyboard = create_back_to_menu_keyboard_button()
            
            await status_message.edit(
                f'<b>✅ Успешно</b>\n\n'
                f'<b>🤖</b> @{bot_username}\n'
                f'<b>📋 Статус:</b> Работает',
                buttons=back_keyboard,
                parse_mode='html'
            )
        except Exception as error:
            await status_message.edit(
                f'<b>❌ Ошибка:</b> {error}',
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА БАНА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_ban' and is_user_admin(user_id):
        parts = message_text.split(' ', 1)
        if len(parts) >= 1 and parts[0].isdigit():
            target_user_id = int(parts[0])
            reason = parts[1] if len(parts) > 1 else 'Нарушение правил'
            
            ban_user(target_user_id, reason, user_id)
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            
            await event.respond(
                f'<b>✅ ПОЛЬЗОВАТЕЛЬ ЗАБАНЕН</b>\n\n'
                f'<b>ID:</b> <code>{target_user_id}</code>\n'
                f'<b>Причина:</b> {reason}',
                buttons=admin_keyboard,
                parse_mode='html'
            )
            
            try:
                await telegram_bot.send_message(
                    target_user_id,
                    f'<b>⛔ ВЫ ЗАБЛОКИРОВАНЫ</b>\n\n'
                    f'<b>Причина:</b> {reason}\n\n'
                    f'<i>Обратитесь к администратору: {OWNER_USERNAME}</i>',
                    parse_mode='html'
                )
            except Exception:
                pass
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат.</b>\n\n'
                '<i>Пример: 123456789 спам</i>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА МУТА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_mute' and is_user_admin(user_id):
        parts = message_text.split(' ', 2)
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            target_user_id = int(parts[0])
            minutes = int(parts[1])
            reason = parts[2] if len(parts) > 2 else 'Нарушение правил'
            
            admin_level = get_admin_level(user_id)
            max_minutes = ADMIN_PERMISSIONS.get(admin_level, {}).get('max_mute_minutes', 0)
            
            if minutes > max_minutes:
                await event.respond(
                    f'<b>⛔ ПРЕВЫШЕН ЛИМИТ</b>\n\n'
                    f'<b>Максимум для вашего уровня:</b> {max_minutes} минут',
                    parse_mode='html'
                )
                return
            
            mute_user(target_user_id, minutes, reason, user_id)
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            
            await event.respond(
                f'<b>✅ ПОЛЬЗОВАТЕЛЬ ЗАМЬЮЧЕН</b>\n\n'
                f'<b>ID:</b> <code>{target_user_id}</code>\n'
                f'<b>Срок:</b> {minutes} минут\n'
                f'<b>Причина:</b> {reason}',
                buttons=admin_keyboard,
                parse_mode='html'
            )
            
            try:
                await telegram_bot.send_message(
                    target_user_id,
                    f'<b>🔇 ВЫ ЗАМЬЮЧЕНЫ</b>\n\n'
                    f'<b>Причина:</b> {reason}\n'
                    f'<b>Срок:</b> {minutes} минут\n\n'
                    f'<i>Ожидайте окончания мута</i>',
                    parse_mode='html'
                )
            except Exception:
                pass
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат.</b>\n\n'
                '<i>Пример: 123456789 60 спам</i>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА РАЗБАНА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_unban' and is_user_admin(user_id):
        if message_text.isdigit():
            target_user_id = int(message_text)
            
            if unban_user(target_user_id):
                result_message = f'<b>✅ ПОЛЬЗОВАТЕЛЬ РАЗБАНЕН</b>\n\n<b>ID:</b> <code>{target_user_id}</code>'
            else:
                result_message = f'<b>❌ ПОЛЬЗОВАТЕЛЬ НЕ В БАНЕ</b>\n\n<b>ID:</b> <code>{target_user_id}</code>'
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            await event.respond(result_message, buttons=admin_keyboard, parse_mode='html')
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный ID.</b>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА РАЗМУТА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_unmute' and is_user_admin(user_id):
        if message_text.isdigit():
            target_user_id = int(message_text)
            
            if unmute_user(target_user_id):
                result_message = f'<b>✅ ПОЛЬЗОВАТЕЛЬ РАЗМЬЮЧЕН</b>\n\n<b>ID:</b> <code>{target_user_id}</code>'
            else:
                result_message = f'<b>❌ ПОЛЬЗОВАТЕЛЬ НЕ В МУТЕ</b>\n\n<b>ID:</b> <code>{target_user_id}</code>'
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            await event.respond(result_message, buttons=admin_keyboard, parse_mode='html')
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный ID.</b>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА ПОВЫШЕНИЯ
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_promote' and is_user_admin(user_id):
        parts = message_text.split()
        
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            target_user_id = int(parts[0])
            new_level = int(parts[1])
            
            if not can_admin_promote_to(user_id, new_level):
                await event.respond(
                    '<b>⛔ НЕДОСТАТОЧНО ПРАВ</b>\n\n'
                    f'<b>Вы можете повысить до уровня:</b> {ADMIN_PERMISSIONS.get(get_admin_level(user_id), {}).get("can_promote_to", 0)}',
                    parse_mode='html'
                )
                return
            
            if new_level >= get_admin_level(user_id):
                await event.respond(
                    '<b>⛔ НЕЛЬЗЯ ВЫДАТЬ УРОВЕНЬ ВЫШЕ ИЛИ РАВНЫЙ СВОЕМУ</b>',
                    parse_mode='html'
                )
                return
            
            old_level = get_admin_level(target_user_id)
            admins[target_user_id] = {
                'level': new_level,
                'added_by': user_id,
                'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_admins_to_file()
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            
            await event.respond(
                f'<b>✅ ПОЛЬЗОВАТЕЛЬ ПОВЫШЕН</b>\n\n'
                f'<b>ID:</b> <code>{target_user_id}</code>\n'
                f'<b>Было:</b> {ADMIN_LEVEL_NAMES.get(old_level, "Не админ")}\n'
                f'<b>Стало:</b> {ADMIN_LEVEL_NAMES.get(new_level, "Неизвестно")}',
                buttons=admin_keyboard,
                parse_mode='html'
            )
            
            try:
                await telegram_bot.send_message(
                    OWNER_ID,
                    f'<b>⬆ ПОВЫШЕНИЕ</b>\n\n'
                    f'<b>Кто:</b> <code>{target_user_id}</code>\n'
                    f'<b>Новый уровень:</b> {new_level} — {ADMIN_LEVEL_NAMES.get(new_level, "?")}\n'
                    f'<b>Кем:</b> <code>{user_id}</code>\n'
                    f'<b>Дата:</b> {datetime.now().strftime("%d.%m.%Y %H:%M")}',
                    parse_mode='html'
                )
            except Exception:
                pass
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат.</b>\n\n'
                '<i>Пример: 123456789 3</i>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА ПОНИЖЕНИЯ
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_demote' and is_user_admin(user_id):
        parts = message_text.split()
        
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            target_user_id = int(parts[0])
            new_level = int(parts[1])
            
            if target_user_id == OWNER_ID:
                await event.respond(
                    '<b>⛔ НЕЛЬЗЯ ПОНИЗИТЬ ВЛАДЕЛЬЦА</b>',
                    parse_mode='html'
                )
                return
            
            if get_admin_level(target_user_id) >= get_admin_level(user_id):
                await event.respond(
                    '<b>⛔ НЕЛЬЗЯ ПОНИЗИТЬ РАВНОГО ИЛИ ВЫШЕ</b>',
                    parse_mode='html'
                )
                return
            
            old_level = get_admin_level(target_user_id)
            admins[target_user_id] = {
                'level': new_level,
                'added_by': user_id,
                'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_admins_to_file()
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            
            await event.respond(
                f'<b>✅ ПОЛЬЗОВАТЕЛЬ ПОНИЖЕН</b>\n\n'
                f'<b>ID:</b> <code>{target_user_id}</code>\n'
                f'<b>Было:</b> {ADMIN_LEVEL_NAMES.get(old_level, "?")}\n'
                f'<b>Стало:</b> {ADMIN_LEVEL_NAMES.get(new_level, "?")}',
                buttons=admin_keyboard,
                parse_mode='html'
            )
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный формат.</b>\n\n'
                '<i>Пример: 123456789 1</i>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА ПОДАРКА ПОДПИСКИ
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_gift_sub' and is_user_admin(user_id):
        if message_text.isdigit():
            target_user_id = int(message_text)
            user_subscriptions[target_user_id] = True
            
            user_states[user_id] = None
            admin_keyboard = create_admin_panel_keyboard_for_user(user_id)
            
            await event.respond(
                f'<b>✅ ПОДПИСКА ПОДАРЕНА</b>\n\n'
                f'<b>Пользователь:</b> <code>{target_user_id}</code>\n'
                f'<b>Теперь у него безлимитные запросы.</b>',
                buttons=admin_keyboard,
                parse_mode='html'
            )
            
            try:
                await telegram_bot.send_message(
                    target_user_id,
                    '<b>🎁 ВАМ ПОДАРИЛИ ПОДПИСКУ!</b>\n\n'
                    '<b>Теперь у вас безлимитные запросы.</b>',
                    parse_mode='html'
                )
            except Exception:
                pass
        else:
            cancel_keyboard = create_cancel_keyboard_button()
            await event.respond(
                '<b>❌ Неверный ID.</b>',
                buttons=cancel_keyboard,
                parse_mode='html'
            )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА РАССЫЛКИ
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_broadcast' and is_user_admin(user_id):
        admin_level = get_admin_level(user_id)
        if not ADMIN_PERMISSIONS.get(admin_level, {}).get('can_broadcast', False):
            return
        
        user_states[user_id] = None
        back_keyboard = create_back_to_menu_keyboard_button()
        
        await event.respond(
            f'<b>📢 РАССЫЛКА ВЫПОЛНЕНА</b>\n\n'
            f'<b>Сообщение:</b>\n{message_text[:500]}',
            buttons=back_keyboard,
            parse_mode='html'
        )
    
    # ═══════════════════════════════════════════════════════════════════════════════════
    # ОБРАБОТКА БЕЛОГО СПИСКА
    # ═══════════════════════════════════════════════════════════════════════════════════
    
    elif current_state == 'waiting_whitelist' and is_user_admin(user_id):
        data = {}
        for line in message_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        phone = data.get('Номер', '')
        if not phone:
            found_phones = re.findall(r'\+?\d{10,12}', message_text)
            if found_phones:
                phone = found_phones[0]
        
        if phone:
            save_to_whitelist_file(phone, {
                'data': data,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            user_states[user_id] = None
            back_keyboard = create_back_to_menu_keyboard_button()
            
            await event.respond(
                f'<b>✅ ДОБАВЛЕНО В БЕЛЫЙ СПИСОК</b>\n\n'
                f'<b>Номер:</b> {phone}',
                buttons=back_keyboard,
                parse_mode='html'
            )
        else:
            back_keyboard = create_back_to_menu_keyboard_button()
            await event.respond(
                '<b>❌ Номер не найден.</b>\n\n'
                '<i>Укажите номер в формате: Номер: +79999999999</i>',
                buttons=back_keyboard,
                parse_mode='html'
            )

# ═══════════════════════════════════════════════════════════════════════════════════════
# ЗАПУСК БОТА
# ═══════════════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("""╔══════════════════════════════════════╗
║                                      ║
║   🕵️  DIX PROBIV BOT v5.0           ║
║   Проект #Амнезия                   ║
║   Dixyi © 2025                       ║
║                                      ║
║   7 уровней администраторов          ║
║   Подписка, рефералы, лимиты         ║
║   Анти-флуд защита                   ║
║   Зеркала, белый список              ║
║                                      ║
╚══════════════════════════════════════╝
    """)
    
    # Создаём папки
    os.makedirs(MIRRORS_FOLDER, exist_ok=True)
    os.makedirs(LOGS_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    
    log_info_message('Бот запущен и готов к работе')
    log_info_message(f'Владелец: {OWNER_ID}')
    log_info_message(f'Администраторов: {len(admins)}')
    
    # Запускаем зеркала
    mirrors = get_mirrors_list_from_file()
    if mirrors:
        for token, info in mirrors.items():
            username = info.get('username', 'unknown')
            mirror_script = os.path.join(MIRRORS_FOLDER, f'mirror_{username}.py')
            if os.path.exists(mirror_script):
                try:
                    import subprocess
                    subprocess.Popen(
                        [sys.executable, mirror_script],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                    log_info_message(f'Зеркало @{username} запущено')
                except Exception as error:
                    log_error_message(f'Ошибка запуска зеркала @{username}: {error}')
    
    # Основной цикл
    while True:
        try:
            telegram_bot.run_until_disconnected()
        except FloodWaitError as error:
            log_warning_message(f'FloodWait {error.seconds} секунд. Ожидание...')
            time.sleep(error.seconds + 5)
        except Exception as error:
            log_error_message(f'Критическая ошибка: {error}')
            time.sleep(30)
