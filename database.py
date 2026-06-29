
import sqlite3, json, os, time

DB_PATH = "./dix_results.db"
WHITELIST_FILE = "./dix_whitelist.json"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lookups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        query TEXT,
        result TEXT,
        date TEXT,
        user_id INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        username TEXT,
        requests INTEGER DEFAULT 0,
        first_seen TEXT,
        last_seen TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS mirrors (
        token TEXT PRIMARY KEY,
        name TEXT,
        username TEXT,
        created_date TEXT
    )''')
    conn.commit()
    conn.close()

def save_lookup(lookup_type, query, result, user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO lookups (type, query, result, date, user_id) VALUES (?,?,?,datetime("now","localtime"),?)',
                (lookup_type, query, result, user_id))
    conn.commit()
    conn.close()

def save_user(user_id, first_name, username):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT OR REPLACE INTO users (user_id, first_name, username, requests, last_seen)
                   VALUES (?,?,?,COALESCE((SELECT requests+1 FROM users WHERE user_id=?),1),datetime("now","localtime"))''',
                (user_id, first_name, username, user_id))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM lookups')
    total_lookups = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM mirrors')
    total_mirrors = c.fetchone()[0]
    conn.close()
    return {'lookups': total_lookups, 'users': total_users, 'mirrors': total_mirrors}

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return {}
    with open(WHITELIST_FILE, 'r') as f:
        return json.load(f)

def save_whitelist(data):
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def check_whitelist(phone):
    wl = load_whitelist()
    cleaned = ''.join(filter(str.isdigit, phone))
    return cleaned in wl
