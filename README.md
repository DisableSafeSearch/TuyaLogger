# Пишем логи с умной розетки Tuya

<img width="2634" height="1256" alt="CleanShot 2025-08-06 at 23 45 49@2x" src="https://github.com/user-attachments/assets/f57d2838-68a6-4d8b-90b2-f83aab0adf0f" />

# Установка и использование

1. Устанавливаем виртуальное окружение — ```python3 -m venv venv```
2. Запускаем окружение — Linux/MacOS ```source venv/bin/activate```, Win ```venv\Scripts\activate.bat```
2. Устанавливаем зависимости — ```python3 -m pip install -r requirements.txt```
3. Любыми путями получаем ```local_key```, например при помощи [LocalTuyaKeyExtractor](https://github.com/HiveMindAutomation/LocalTuyaKeyExtractor) или [TuyaKeyExtractor](https://github.com/MarkWattTech/TuyaKeyExtractor)
4. Заполняем поля в файле config.json
5. Запускаем скрипт — ```python3 power_logger.py```

