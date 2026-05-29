import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

def create_backup(file_path: Path) -> Optional[Path]:
    """Создание временной резервной копии"""
    try:
        backup_dir = Path(tempfile.mkdtemp(prefix="ransom_sim_backup_"))
        backup_path = backup_dir / file_path.name
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"[!] Не удалось создать бэкап: {e}")
        return None

def safe_rename(old_path: Path, new_path: Path) -> bool:
    """Безопасное переименование файла"""
    try:
        if new_path.exists():
            return False
        old_path.rename(new_path)
        return True
    except Exception:
        return False

def is_safe_path(path: Path) -> bool:
    """Проверка, не является ли файл критическим системным"""
    critical_paths = [
        "/etc/passwd", "/etc/shadow", "/etc/sudoers",
        "/boot/", "/usr/lib/", "/lib/", "/bin/", "/sbin/"
    ]
    
    str_path = str(path.absolute())
    for critical in critical_paths:
        if str_path.startswith(critical):
            return False
    return True

def get_file_info(file_path: Path) -> dict:
    """Получение метаданных файла"""
    try:
        stat = file_path.stat()
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "permissions": stat.st_mode,
            "owner": stat.st_uid
        }
    except:
        return {}

# Добавляем цвета для вывода
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def color_print(text, color=Colors.GREEN):
    """Цветной вывод в консоль"""
    if sys.stdout.isatty():  # Если терминал поддерживает цвета
        print(f"{color}{text}{Colors.ENDC}")
    else:
        print(text)
