#!/usr/bin/env python3
"""
Linux Ransomware Simulator
Safe simulation of ransomware behavior for security testing
"""

import argparse
import sys
from pathlib import Path
from .config import load_config, Config
from .scanner import FileScanner
from .simulator_engine import RansomwareSimulator
from .persistence import PersistenceSimulator
from .reporter import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Linux Ransomware Simulator - Safe security testing tool"
    )
    parser.add_argument(
        "--target", "-t",
        nargs="+",
        help="Target directories (overrides config)"
    )
    parser.add_argument(
        "--simulate", "-s",
        action="store_true",
        help="Enable real simulation (default is dry-run)"
    )
    parser.add_argument(
        "--no-persistence",
        action="store_true",
        help="Skip persistence simulation"
    )
    parser.add_argument(
        "--no-shadow",
        action="store_true",
        help="Skip shadow copy simulation"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--max-files", "-m",
        type=int,
        default=0,
        help="Maximum files to process (0 = unlimited)"
    )
    
    args = parser.parse_args()
    
    # Загрузка конфигурации
    config = load_config()
    
    # Переопределение параметров
    if not args.simulate:
        config.dry_run = True
    else:
        config.dry_run = False
    
    if args.target:
        config.target_dirs = args.target
    
    if args.no_shadow:
        config.delete_shadows = False
    
    print("""
    ╔════════════════════════════════════════╗
    ║   Linux Ransomware Simulator v1.0     ║
    ║   SAFE MODE: ACTIVE                    ║
    ║   No actual encryption performed       ║
    ╚════════════════════════════════════════╝
    """)
    
    print(f"[*] Режим: {'DRY-RUN (безопасный)' if config.dry_run else 'SIMULATION'}")
    print(f"[*] Целевые директории: {config.target_dirs}")
    print(f"[*] Расширения: {len(config.target_extensions)} типов файлов")
    
    # Шаг 1: Сканирование
    scanner = FileScanner(config)
    files = scanner.scan()
    
    if args.max_files > 0 and len(files) > args.max_files:
        print(f"[*] Ограничение до {args.max_files} файлов")
        files = files[:args.max_files]
    
    # Шаг 2: Симуляция шифрования
    simulator = RansomwareSimulator(config)
    encryption_results = simulator.simulate_encryption(files)
    
    # Шаг 3: Записка вымогателя
    simulator.create_ransom_note()
    
    # Шаг 4: Удаление теневых копий
    simulator.simulate_shadow_deletion()
    
    # Шаг 5: Завершение процессов
    killed = simulator.simulate_process_termination()
    
    # Шаг 6: Закрепление в системе
    persistence_methods = []
    if not args.no_persistence:
        persister = PersistenceSimulator(config)
        persistence_methods = persister.simulate_all()
    
    # Шаг 7: Генерация отчёта
    report_data = {
        "scanned": scanner.scanned_files,
        "encrypted": encryption_results["encrypted"],
        "failed": encryption_results["failed"],
        "encrypted_list": [r["file"] for r in encryption_results["details"] if r["status"] == "encrypted"],
        "ransom_note": simulator.ransom_note_created,
        "shadows_deleted": simulator.vss_deleted
    }
    
    reporter = ReportGenerator(config)
    report_path = reporter.generate_report(
        {"scanned": scanner.scanned_files},
        report_data,
        persistence_methods,
        killed
    )
    
    print(f"\n[✓] Симуляция завершена. Отчёт: {report_path}")
    
    # Полезные советы
    print("""
    
    ════════════════════════════════════════
    ЧТО ДЕЛАТЬ, ЕСЛИ ЭТО БЫЛА РЕАЛЬНАЯ АТАКА:
    1. НЕ платить выкуп
    2. Отключить заражённую систему от сети
    3. Сообщить в ИБ-отдел
    4. Сохранить логи и зашифрованные файлы
    5. Восстанавливаться из бэкапов
    ════════════════════════════════════════
    """)

if __name__ == "__main__":
    main()
