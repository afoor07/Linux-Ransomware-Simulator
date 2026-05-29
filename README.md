# 🦠 Linux Ransomware Simulator

[![Security](https://img.shields.io/badge/Security-Testing-red)](https://github.com/afoor07/linux-ransomware-simulator)
[![Python](https://img.shields.io/badge/Python-3.6+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)](https://linux.org)

> ⚠️ **Только для образовательных целей!** Никакого реального шифрования файлов не происходит.

Безопасный симулятор поведения ransomware для тестирования EDR, антивирусов, SIEM систем.

## 🎬 Демонстрация

```bash
$ python3 -m simulator.main --simulate --target ~/Documents

╔════════════════════════════════════════╗
║   Linux Ransomware Simulator v1.0      ║
║   SAFE MODE: ACTIVE                    ║
║   No actual encryption performed       ║
╚════════════════════════════════════════╝

[*] Режим: SIMULATION
[*] Найдено целевых файлов: 157
[*] Симуляция атаки...
[+] 'Зашифровано': 157 файлов
[+] Создана записка вымогателя
[✓] Отчёт сохранён: reports/report_20241215_120000.txt
```

## ✨ Возможности

### 🔍 Сканирование
- Обход целевых директорий (Documents, Downloads, Desktop)
- Фильтрация по расширениям (doc, pdf, xls, txt, sql, и т.д.)
- Исключение системных путей (/etc, /usr, /proc)
- Ограничение по размеру файлов

### 💀 Симуляция атаки
- **Dry-run режим** (безопасный, только логирование)
- **Simulation режим** (переименование файлов в .encrypted)
- Создание фальшивой записки вымогателя
- Симуляция удаления теневых копий (VSS)
- Завершение критических процессов (базы данных, офис)

### 🔄 Механизмы закрепления (Persistence)
- Добавление в crontab
- Создание systemd сервиса
- Инъекция в .bashrc
- Бэкдор через SSH ключи
- LD_PRELOAD (обнаружение)

### 📊 Отчётность
- Детальные JSON отчёты
- Человеко-читаемые TXT отчёты
- Рекомендации по защите
- Список "потерянных" файлов

## 🚀 Установка

### Быстрая установка

```bash
# Клонирование репозитория
git clone https://github.com/afoor07/linux-ransomware-simulator.git
cd linux-ransomware-simulator

# Установка зависимостей
pip3 install -r requirements.txt

# Или через make
make install
```

### Docker (альтернативный способ)

```bash
docker build -t ransomware-sim .
docker run --rm -v /tmp:/tmp ransomware-sim --simulate --target /tmp/test
```

## 🎮 Использование

### Основные команды

```bash
# Безопасный режим (dry-run) - по умолчанию
python3 -m simulator.main

# Полная симуляция (переименование файлов)
python3 -m simulator.main --simulate --target /path/to/dir

# Сканирование конкретных директорий
python3 -m simulator.main --target /home/user/docs /var/www

# Без симуляции закрепления в системе
python3 -m simulator.main --simulate --no-persistence

# Без симуляции удаления теневых копий
python3 -m simulator.main --simulate --no-shadow

# Ограничение количества файлов
python3 -m simulator.main --simulate --max-files 100

# Вербозный режим (детальный вывод)
python3 -m simulator.main --simulate --verbose
```

### Make команды

```bash
make install          # Установка зависимостей
make run-dry          # Dry-run режим
make run-simulate     # Полная симуляция
make run-full-test    # Тест с временными файлами
make clean           # Очистка временных файлов
make test            # Запуск тестов
```

## 📝 Примеры

### Пример 1: Тестирование на тестовых файлах

```bash
# Создаём тестовые файлы
mkdir -p /tmp/ransom_test
echo "Confidential data" > /tmp/ransom_test/document.txt
echo "SELECT * FROM users" > /tmp/ransom_test/database.sql

# Запускаем симуляцию
python3 -m simulator.main --simulate --target /tmp/ransom_test

# Проверяем результат
ls -la /tmp/ransom_test/
# Вы увидите: document.txt.encrypted, database.sql.encrypted, README_RECOVERY.txt
```

### Пример 2: Интеграция с системой мониторинга

```bash
# Сохраняем отчёт для дальнейшего анализа
python3 -m simulator.main --simulate --target ~/Documents
cat reports/report_*.json | jq '.summary'
```

### Пример 3: Автоматизация через cron

```bash
# Еженедельное тестирование
0 2 * * 1 cd /home/user/linux-ransomware-simulator && python3 -m simulator.main --simulate --target /home/user/documents --max-files 50
```

## 📁 Структура проекта

```bash
linux-ransomware-simulator/
├── simulator/
│   ├── __init__.py
│   ├── main.py              # Точка входа
│   ├── config.py            # Конфигурация
│   ├── scanner.py           # Сканер файлов
│   ├── simulator_engine.py  # Движок симуляции
│   ├── persistence.py       # Закрепление в системе
│   ├── reporter.py          # Генерация отчётов
│   └── utils.py             # Вспомогательные функции
├── tests/                   # Модульные тесты
├── reports/                 # Директория с отчётами
├── requirements.txt         # Зависимости
├── Makefile                # Make команды
├── setup.py                # Установка пакета
└── README.md               # Документация
```

## 🎯 Сценарии использования

### 1. Тестирование EDR/SIEM систем
- Проверка срабатывания на массовое переименование
- Тестирование правил корреляции
- Обучение SOC аналитиков

### 2. Аудит резервного копирования
- Проверка, что бэкапы защищены от шифрования
- Тестирование времени восстановления
- Валидация offline backup policy

### 3. Обучение персонала
- Демонстрация реального поведения ransomware
- Тренировка реагирования на инцидент
- Понимание тактик и техник MITRE ATT&CK

### 4. Настройка политик безопасности
- Проверка AppLocker/SELinux правил
- Тестирование минимальных привилегий
- Аудит прав доступа

## 🛡️ Безопасность

### Гарантии безопасности
- ✅ **Файлы не шифруются** (только переименование в simulation режиме)
- ✅ **Оригиналы сохраняются** (временные бэкапы)
- ✅ **Dry-run по умолчанию** (ничего не меняется)
- ✅ **Safe mode** (системные файлы не трогаются)
- ✅ **Бэкапы восстанавливаются** автоматически

### Что НЕ делает симулятор
- ❌ Не шифрует файлы реально
- ❌ Не удаляет оригиналы
- ❌ Не отправляет данные вовне
- ❌ Не создаёт сетевые соединения
- ❌ Не выполняет вредоносный код

## 📄 Лицензия

MIT License - только для образовательных целей.

```bash
MIT License

Copyright (c) 2024 afoor07

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📧 Контакты

- **Автор**: afoor07
- **GitHub**: [github.com/afoor07](https://github.com/afoor07)
- **Проект**: [linux-ransomware-simulator](https://github.com/afoor07/linux-ransomware-simulator)
