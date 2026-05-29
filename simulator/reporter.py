import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from .config import Config

class ReportGenerator:
    """Генерация отчётов"""
    
    def __init__(self, config: Config):
        self.config = config
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)
    
    def generate_report(self, scan_results: Dict, simulation_results: Dict, 
                       persistence_methods: List[str], killed_processes: List[str]) -> Path:
        """Генерация полного отчёта"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "mode": "DRY_RUN" if self.config.dry_run else "SIMULATION",
            "safe_mode": self.config.safe_mode,
            "summary": {
                "files_scanned": scan_results.get("scanned", 0),
                "files_encrypted": simulation_results.get("encrypted", 0),
                "files_failed": simulation_results.get("failed", 0),
                "ransom_note_created": simulation_results.get("ransom_note", False),
                "shadows_deleted": simulation_results.get("shadows_deleted", False),
                "persistence_methods": len(persistence_methods),
                "processes_killed": len(killed_processes)
            },
            "details": {
                "target_directories": self.config.target_dirs,
                "file_extensions": self.config.target_extensions,
                "encrypted_files": simulation_results.get("encrypted_list", [])[:100],  # Первые 100
                "persistence_methods": persistence_methods,
                "processes_killed": killed_processes
            },
            "recommendations": self._generate_recommendations(simulation_results, persistence_methods)
        }
        
        # Сохраняем JSON
        json_path = self.report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Сохраняем человеко-читаемый отчёт
        txt_path = self.report_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self._save_text_report(report, txt_path)
        
        print(f"\n[+] Отчёты сохранены:")
        print(f"    - JSON: {json_path}")
        print(f"    - TXT: {txt_path}")
        
        return txt_path
    
    def _generate_recommendations(self, simulation_results: Dict, persistence_methods: List[str]) -> List[str]:
        """Генерация рекомендаций по защите"""
        recommendations = []
        
        if simulation_results.get("encrypted", 0) > 0:
            recommendations.append("Настроить регулярное резервное копирование (правило 3-2-1)")
            recommendations.append("Включить File System Audit и мониторинг массового переименования")
        
        if simulation_results.get("shadows_deleted", False):
            recommendations.append("Ограничить доступ к vssadmin и wmic через AppLocker/SELinux")
            recommendations.append("Настроить алерты на удаление теневых копий")
        
        if persistence_methods:
            recommendations.append("Регулярно проверять crontab, systemd, .bashrc на изменения")
            recommendations.append("Использовать AIDE или Tripwire для контроля целостности")
            recommendations.append("Настроить мониторинг /etc/ld.so.preload и ~/.ssh/authorized_keys")
        
        if self.config.dry_run:
            recommendations.append("Запустите в режиме --simulate для проверки EDR")
        
        recommendations.append("Провести обучение пользователей по фишинговым атакам")
        
        return recommendations
    
    def _save_text_report(self, report: Dict, path: Path):
        """Сохранение текстового отчёта"""
        content = f"""
========================================
   RANSOMWARE SIMULATION REPORT
========================================

Time: {report['timestamp']}
Mode: {report['mode']}
Safe Mode: {report['safe_mode']}

--- SUMMARY ---
Files Scanned: {report['summary']['files_scanned']}
Files 'Encrypted': {report['summary']['files_encrypted']}
Files Failed: {report['summary']['files_failed']}
Ransom Note Created: {report['summary']['ransom_note_created']}
Shadows Deleted: {report['summary']['shadows_deleted']}
Persistence Methods: {report['summary']['persistence_methods']}
Processes Killed: {report['summary']['processes_killed']}

--- TARGETS ---
Directories: {', '.join(report['details']['target_directories'])}
Extensions: {', '.join(report['details']['file_extensions'])}

--- PERSISTENCE METHODS ---
{chr(10).join(f'  - {m}' for m in report['details']['persistence_methods'])}

--- KILLED PROCESSES ---
{chr(10).join(f'  - {p}' for p in report['details']['processes_killed']) if report['details']['processes_killed'] else '  None'}

--- AFFECTED FILES (first 20) ---
{chr(10).join(f'  - {f}' for f in report['details']['encrypted_files'][:20])}

--- RECOMMENDATIONS ---
{chr(10).join(f'  {i+1}. {r}' for i, r in enumerate(report['recommendations']))}

========================================
"""
        path.write_text(content)
