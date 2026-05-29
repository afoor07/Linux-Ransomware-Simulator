import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Config:
    """Конфигурация симулятора"""
    
    # Режимы работы
    dry_run: bool = True  # Безопасный режим (только логи)
    simulate_encryption: bool = True  # Симулировать переименование
    simulate_file_deletion: bool = False  # Не удаляем реально
    
    # Целевые директории
    target_dirs: List[str] = None
    excluded_dirs: List[str] = None
    
    # Расширения файлов-жертв
    target_extensions: List[str] = None
    
    # Симуляция поведения
    ransom_note_name: str = "README_RECOVERY.txt"
    encrypted_extension: str = ".encrypted"
    delete_shadows: bool = True  # Симулировать удаление теневых копий
    kill_processes: bool = True   # Симулировать завершение процессов
    
    # Параметры безопасности
    max_file_size_mb: int = 10
    min_file_age_days: int = 0
    safe_mode: bool = True  # Защищённый режим (не трогает системные файлы)
    
    def __post_init__(self):
        if self.target_dirs is None:
            self.target_dirs = [
                str(Path.home() / "Documents"),
                str(Path.home() / "Downloads"),
                str(Path.home() / "Desktop"),
                "/tmp/ransom_sim_test"  # Тестовая папка
            ]
        
        if self.excluded_dirs is None:
            self.excluded_dirs = [
                "/etc", "/usr", "/boot", "/proc", "/sys",
                "/dev", "/var/log", "/run", "/root/.ssh"
            ]
        
        if self.target_extensions is None:
            self.target_extensions = [
                ".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx",
                ".jpg", ".png", ".mp4", ".mp3", ".zip", ".tar",
                ".gz", ".db", ".sql", ".conf", ".log", ".sh"
            ]

def load_config() -> Config:
    """Загрузка конфигурации из env"""
    config = Config()
    
    # Переопределение через переменные окружения
    if os.getenv("SIM_DRY_RUN") is not None:
        config.dry_run = os.getenv("SIM_DRY_RUN", "true").lower() == "true"
    
    if os.getenv("SIM_SAFE_MODE") is not None:
        config.safe_mode = os.getenv("SIM_SAFE_MODE", "true").lower() == "true"
    
    return config
