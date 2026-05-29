import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List
from .config import Config
from .utils import create_backup, safe_rename

class RansomwareSimulator:
    """Симуляция действий ransomware"""
    
    def __init__(self, config: Config):
        self.config = config
        self.encrypted_files = []
        self.ransom_note_created = False
        self.vss_deleted = False
        self.processes_killed = []
    
    def simulate_encryption(self, files: List[Path]) -> dict:
        """Симуляция шифрования файлов"""
        results = {
            "encrypted": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }
        
        print(f"\n[*] Начинаем симуляцию атаки на {len(files)} файлов...")
        
        for idx, file_path in enumerate(files, 1):
            try:
                result = self._process_file(file_path)
                results[result["status"]] += 1
                results["details"].append(result)
                
                if idx % 100 == 0:
                    print(f"[*] Прогресс: {idx}/{len(files)}")
                    
            except Exception as e:
                print(f"[!] Ошибка с файлом {file_path}: {e}")
                results["failed"] += 1
        
        print(f"\n[+] Симуляция завершена:")
        print(f"    - 'Зашифровано': {results['encrypted']}")
        print(f"    - Пропущено: {results['skipped']}")
        print(f"    - Ошибок: {results['failed']}")
        
        return results
    
    def _process_file(self, file_path: Path) -> dict:
        """Обработка одного файла"""
        result = {
            "file": str(file_path),
            "status": "skipped",
            "message": "",
            "timestamp": datetime.now().isoformat()
        }
        
        if self.config.dry_run:
            result["message"] = f"[DRY RUN] Был бы зашифрован: {file_path}"
            result["status"] = "encrypted"
            return result
        
        if self.config.simulate_encryption:
            # Создаём резервную копию для безопасности
            backup_path = create_backup(file_path)
            
            # Симулируем переименование
            new_path = file_path.with_suffix(
                file_path.suffix + self.config.encrypted_extension
            )
            
            if safe_rename(file_path, new_path):
                result["message"] = f"Симулировано шифрование: {file_path} -> {new_path}"
                result["status"] = "encrypted"
                self.encrypted_files.append(new_path)
            else:
                result["message"] = f"Не удалось переименовать: {file_path}"
                result["status"] = "failed"
            
            # Восстанавлием оригинал в тестовом режиме
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, file_path)
                backup_path.unlink()
        else:
            result["message"] = f"Пропущен (симуляция отключена): {file_path}"
        
        return result
    
    def create_ransom_note(self) -> bool:
        """Создание фальшивой записки вымогателей"""
        if self.config.dry_run:
            print("[DRY RUN] Была бы создана записка вымогателя")
            return True
        
        ransom_content = f"""
========================================
    WARNING! YOUR FILES ARE ENCRYPTED
========================================

This is a SIMULATION for security testing purposes.

In a real ransomware attack, all your important files would be encrypted.

What happened?
- All your documents, images, and databases have been encrypted
- Shadow copies have been deleted
- Recovery is impossible without the decryption key

To prevent REAL attacks:
1. Maintain offline backups
2. Keep systems patched
3. Use EDR solution
4. Implement least privilege access

SIMULATION INFO:
- Time: {datetime.now()}
- Files affected: {len(self.encrypted_files)}
- No actual encryption occurred
- No payment required

This is a security drill. Contact your IT security team.
========================================
"""
        
        for target_dir in self.config.target_dirs:
            if os.path.exists(target_dir):
                note_path = Path(target_dir) / self.config.ransom_note_name
                try:
                    note_path.write_text(ransom_content)
                    print(f"[+] Создана записка: {note_path}")
                except Exception as e:
                    print(f"[!] Не удалось создать записку в {target_dir}: {e}")
        
        self.ransom_note_created = True
        return True
    
    def simulate_shadow_deletion(self) -> bool:
        """Симуляция удаления теневых копий"""
        if not self.config.delete_shadows:
            return False
        
        print("\n[*] Симуляция удаления теневых копий (VSS)...")
        
        if self.config.dry_run:
            print("[DRY RUN] Была бы выполнена команда: vssadmin delete shadows /all /quiet")
            self.vss_deleted = True
            return True
        
        # Проверяем наличие vssadmin
        vssadmin_path = shutil.which("vssadmin")
        if vssadmin_path:
            print(f"[!] Обнаружен vssadmin, но команда не выполняется (симуляция)")
            print("    В реальной атаке: vssadmin delete shadows /all /quiet")
        
        # Симуляция через логирование
        print("[SIM] Выполнено: удаление всех теневых копий")
        print("[SIM] Выполнено: отключение восстановления системы")
        
        self.vss_deleted = True
        return True
    
    def simulate_process_termination(self) -> List[str]:
        """Симуляция завершения процессов (базы данных, офис)"""
        if not self.config.kill_processes:
            return []
        
        print("\n[*] Симуляция завершения процессов...")
        
        target_processes = [
            "sql", "mysql", "postgres", "oracle",
            "word", "excel", "outlook", "libreoffice",
            "backup", "ntp", "teamviewer"
        ]
        
        killed = []
        for proc_name in target_processes:
            if self.config.dry_run:
                killed.append(proc_name)
                print(f"[DRY RUN] Был бы завершён процесс: {proc_name}")
            else:
                # Проверяем реальные процессы через /proc
                import subprocess
                try:
                    result = subprocess.run(
                        ["pgrep", "-f", proc_name],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        pids = result.stdout.strip().split()
                        killed.extend([f"{proc_name}(PID={pid})" for pid in pids])
                        print(f"[SIM] Найден процесс {proc_name}: PIDs={pids}")
                except:
                    pass
        
        self.processes_killed = killed
        return killed
