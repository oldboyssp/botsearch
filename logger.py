
import os, time
from datetime import datetime

LOG_DIR = "./logs"
LOG_FILE = f"{LOG_DIR}/bot.log"
ERROR_FILE = f"{LOG_DIR}/errors.log"
ACCESS_FILE = f"{LOG_DIR}/access.log"

os.makedirs(LOG_DIR, exist_ok=True)

def log(level, message, file='bot'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = f"[{timestamp}] [{level}] {message}"
    print(text)
    
    logfile = LOG_FILE if file == 'bot' else (ERROR_FILE if file == 'error' else ACCESS_FILE)
    try:
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
    except:
        pass

def info(msg):
    log('INFO', msg)

def warning(msg):
    log('WARNING', msg)

def error(msg):
    log('ERROR', msg, 'error')

def access(user_id, action):
    log('ACCESS', f'User {user_id} — {action}', 'access')

def get_logs(lines=50):
    if not os.path.exists(LOG_FILE):
        return 'Логов нет'
    with open(LOG_FILE, 'r') as f:
        all_lines = f.readlines()
        return ''.join(all_lines[-lines:])

def get_errors(lines=50):
    if not os.path.exists(ERROR_FILE):
        return 'Ошибок нет'
    with open(ERROR_FILE, 'r') as f:
        all_lines = f.readlines()
        return ''.join(all_lines[-lines:])

def clear_logs():
    for f in [LOG_FILE, ERROR_FILE, ACCESS_FILE]:
        if os.path.exists(f):
            open(f, 'w').close()
