import os
import stat
from pathlib import Path
from typing import List
from .config import Config

class PersistenceSimulator:
    """Симуляция закрепления в системе"""
    
    def __init__(self, config: Config):
        self.config = config
        self.persistence_methods = []
    
    def simulate_all(self) -> List[str]:
        """Симуляция всех методов закрепления"""
        print("\n[*] Симуляция механизмов закрепления...")
        
        methods = [
            self._simulate_cron_job,
            self._simulate_systemd_service,
            self._simulate_ssh_key_backdoor,
            self._simulate_bashrc_injection,
            self._simulate_ld_preload
        ]
        
        for method in methods:
            try:
                method()
            except Exception as e:
                print(f"[!] Ошибка в методе {method.__name__}: {e}")
        
        return self.persistence_methods
    
    def _simulate_cron_job(self):
        """Симуляция добавления в crontab"""
        if self.config.dry_run:
            self.persistence_methods.append("cron (simulated)")
            print("[DRY RUN] Добавлена cron-задача: @reboot /path/to/malware")
            return
        
        cron_line = "@reboot /tmp/.system_update.sh >/dev/null 2>&1"
        print(f"[SIM] Потенциальное добавление в crontab: {cron_line}")
        print("      Проверьте: crontab -l")
        
        # Проверяем существующие cron задачи
        try:
            import subprocess
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            if result.stdout:
                print(f"[INFO] Текущие cron-задачи:\n{result.stdout[:200]}...")
        except:
            pass
        
        self.persistence_methods.append("cron_job")
    
    def _simulate_systemd_service(self):
        """Симуляция создания systemd сервиса"""
        service_name = "system-update.service"
        service_content = f"""[Unit]
Description=System Update
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'sleep 60 && /tmp/.system_update.sh'
Restart=always

[Install]
WantedBy=multi-user.target
"""
        
        if self.config.dry_run:
            self.persistence_methods.append("systemd (simulated)")
            print(f"[DRY RUN] Создан systemd сервис: {service_name}")
            return
        
        print(f"[SIM] Симуляция создания сервиса: /etc/systemd/system/{service_name}")
        print(f"[SIM] Содержимое сервиса:\n{service_content}")
        print("      В реальной атаке: systemctl enable", service_name)
        
        self.persistence_methods.append("systemd_service")
    
    def _simulate_ssh_key_backdoor(self):
        """Симуляция добавления SSH ключа"""
        ssh_dir = Path.home() / ".ssh"
        authorized_keys = ssh_dir / "authorized_keys"
        
        fake_key = "ssh-rsa AAAAB3... attacker@backdoor"
        
        if self.config.dry_run:
            self.persistence_methods.append("ssh_backdoor (simulated)")
            print("[DRY RUN] Добавлен SSH ключ в authorized_keys")
            return
        
        if authorized_keys.exists():
            print(f"[SIM] Найден authorized_keys: {authorized_keys}")
            print(f"[SIM] Мог быть добавлен ключ: {fake_key[:50]}...")
            print("      Проверьте integrity файла!")
        else:
            print(f"[WARN] Файл {authorized_keys} не существует")
        
        self.persistence_methods.append("ssh_key_backdoor")
    
    def _simulate_bashrc_injection(self):
        """Симуляция инъекции в .bashrc"""
        bashrc_path = Path.home() / ".bashrc"
        malicious_line = "\n# System update\n(sleep 60 && /tmp/.system_update.sh) &\n"
        
        if self.config.dry_run:
            self.persistence_methods.append("bashrc_injection (simulated)")
            print("[DRY RUN] Инъекция в .bashrc для выполнения при каждом входе")
            return
        
        if bashrc_path.exists():
            content = bashrc_path.read_text()
            if "system_update.sh" not in content:
                print(f"[SIM] Потенциальная инъекция в {bashrc_path}")
                print(f"[SIM] Добавлена строка: {malicious_line.strip()}")
            else:
                print(f"[WARN] {bashrc_path} уже содержит подозрительные строки!")
        else:
            print(f"[INFO] {bashrc_path} не найден")
        
        self.persistence_methods.append("bashrc_injection")
    
    def _simulate_ld_preload(self):
        """Симуляция LD_PRELOAD (перехват библиотек)"""
        if self.config.dry_run:
            self.persistence_methods.append("ld_preload (simulated)")
            print("[DRY RUN] Установлен LD_PRELOAD для перехвата системных вызовов")
            return
        
        ld_preload_file = "/etc/ld.so.preload"
        if os.path.exists(ld_preload_file):
            print(f"[WARN] Обнаружен {ld_preload_file}! Это критично!")
            print("      cat /etc/ld.so.preload")
        else:
            print(f"[SIM] Отсутствует {ld_preload_file} (хороший признак)")
        
        self.persistence_methods.append("ld_preload_check")
