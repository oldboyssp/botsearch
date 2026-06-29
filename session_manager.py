
import os, shutil
from datetime import datetime

SESSION_DIR = "/storage/emulated/0/Download/DIX_SESSION_DATA"

def list_sessions():
    if not os.path.exists(SESSION_DIR):
        return []
    sessions = []
    for f in os.listdir(SESSION_DIR):
        if f.endswith('.session'):
            path = os.path.join(SESSION_DIR, f)
            size = os.path.getsize(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            sessions.append({
                'name': f.replace('.session',''),
                'size': size,
                'modified': mtime.strftime('%d.%m.%Y %H:%M')
            })
    return sessions

def backup_session(name):
    src = os.path.join(SESSION_DIR, f'{name}.session')
    if not os.path.exists(src):
        return False
    backup_dir = os.path.join(SESSION_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    dst = os.path.join(backup_dir, f'{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.session')
    shutil.copy2(src, dst)
    return True

def restore_session(backup_name, target_name):
    backup_dir = os.path.join(SESSION_DIR, 'backups')
    src = os.path.join(backup_dir, backup_name)
    dst = os.path.join(SESSION_DIR, f'{target_name}.session')
    if os.path.exists(src):
        shutil.copy2(src, dst)
        return True
    return False

def delete_session(name):
    path = os.path.join(SESSION_DIR, f'{name}.session')
    journal = os.path.join(SESSION_DIR, f'{name}.session-journal')
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(journal):
        os.remove(journal)
    return True

def session_info(name):
    path = os.path.join(SESSION_DIR, f'{name}.session')
    if not os.path.exists(path):
        return None
    return {
        'name': name,
        'size': os.path.getsize(path),
        'modified': datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d.%m.%Y %H:%M'),
        'exists': True
    }
