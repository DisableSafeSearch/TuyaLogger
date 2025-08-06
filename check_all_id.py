import tinytuya
import json

# Загружаем конфигурацию из внешнего файла
with open('config.json', 'r') as f:
    config = json.load(f)

# Настройки устройства из конфигурационного файла
device_id = config['device_id']
ip = config['ip']
local_key = config['local_key']

# Инициализация устройства
d = tinytuya.OutletDevice(
    dev_id=device_id,
    address=ip,
    local_key=local_key,
    version=3.3,
    persist=True
)

print(" > Запрашиваем статус устройства... < ")
data = d.status()

# Печать полного JSON-ответа
print("\n===== RAW DEVICE STATUS =====")
print(json.dumps(data, indent=4, ensure_ascii=False))

# Выводим отдельно DPS (если есть)
if 'dps' in data:
    print("\n===== DPS (Data Points) =====")
    for key, value in data['dps'].items():
        print(f"ID {key}: {value}")
