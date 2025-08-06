import tinytuya
import time
import csv
import json
import os
from datetime import datetime

# Загружаем конфигурацию
with open('config.json', 'r') as f:
    config = json.load(f)

DEV_ID = config['device_id']
IP = config['ip']
LOCAL_KEY = config['local_key']
INTERVAL = config.get('interval', 10)
CSV_FILE = config.get('csv_file', 'power_log.csv')

# Инициализация устройства
d = tinytuya.OutletDevice(DEV_ID, IP, LOCAL_KEY, version=3.3, persist=True)

# Переменные для логики
power_start_time = None
total_energy_kwh = 0.0

# Создаём заголовок CSV, если файл новый или пустой
need_header = not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0
if need_header:
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Прошло (с)',
            'Дата и время',
            'Ток (А)',
            'Напряжение (В)',
            'Мощность (Вт)',
            'Энергия (кВт·ч)'
        ])

print(" > Запуск. Ожидание связи с устройством...")

def try_get_status():
    try:
        d.status(nowait=True)
        data = d.receive()
        if data and 'dps' in data:
            return data
    except Exception as e:
        print(f"Ошибка запроса: {e}")
    return None

# Ожидаем доступность устройства
while True:
    data = try_get_status()
    if data:
        print(" > Устройство доступно!")
        break
    print(" > Устройство не отвечает, повтор через 5 секунд...")
    time.sleep(5)

print(" > Начинаю запись данных...")

while True:
    data = try_get_status()
    if not data:
        print(" > Потеряна связь с устройством, пробуем через 5 секунд...")
        time.sleep(5)
        continue

    dps = data['dps']
    current_mA = dps.get('18', 0)
    power_mW = dps.get('19', 0)
    voltage_dV = dps.get('20', 0)

    # Преобразование значений
    current = round(current_mA / 1000, 2)
    voltage = round(voltage_dV / 10, 1)
    power = round(power_mW / 10, 1)

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Обнаруживаем старт потребления
    if power_start_time is None and power > 0:
        power_start_time = time.time()
        print(" > Обнаружено потребление — старт отсчёта времени.")

    time_elapsed = round(time.time() - power_start_time) if power_start_time else 0

    # Расчёт энергии — интегрируем мощность
    delta = power * (INTERVAL / 3600)      # Вт * час
    total_energy_kwh += delta / 1000       # Вт·ч → кВт·ч
    energy_kwh = round(total_energy_kwh, 3)

    print(f"[+{time_elapsed}s | {now_str}] "
          f"Ток: {current} А | Напряжение: {voltage} В | "
          f"Мощность: {power} Вт | Энергия: {energy_kwh} кВт·ч")

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            time_elapsed,
            now_str,
            current,
            voltage,
            power,
            energy_kwh
        ])

    time.sleep(INTERVAL)
