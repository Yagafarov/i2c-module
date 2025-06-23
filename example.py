from machine import Pin
from easy_i2c import EasyI2C

# Инициализация I2C шины (SCL - Pin 22, SDA - Pin 21)
i2c = EasyI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# Сканирование I2C шины для поиска подключенных устройств
print("Результаты сканирования I2С:")
devices = i2c.scan(verbose=True)

# Если устройства найдены, берём адрес первого устройства (например, 0x40)
if devices:
    device_addr = devices[0]
    print(f"Выбрано устройство с адресом 0x{device_addr:02X}")
else:
    print("Ошибка: Подключенные устройства не найдены!")
    exit()

# Запись одного байта в регистр (например, 0xFF в регистр 0x01)
try:
    i2c.write_byte(device_addr, 0x01, 0xFF)
    print("В регистр 0x01 записан байт 0xFF")
except OSError as e:
    print(f"Ошибка записи байта: {e}")

# Чтение одного байта из регистра (например, из 0x01)
try:
    value = i2c.read_byte(device_addr, 0x01)
    print(f"Байт, прочитанный из регистра 0x01: 0x{value:02X}")
except OSError as e:
    print(f"Ошибка чтения байта: {e}")

# Запись 16-битного слова в регистр (например, 0x1234 в регистр 0x02)
try:
    i2c.write_word(device_addr, 0x02, 0x1234, byteorder='big')
    print("В регистр 0x02 записано слово 0x1234 (big-endian)")
except OSError as e:
    print(f"Ошибка записи слова: {e}")

# Чтение 16-битного слова из регистра (например, из 0x02)
try:
    word = i2c.read_word(device_addr, 0x02, byteorder='big')
    print(f"Слово, прочитанное из регистра 0x02: 0x{word:04X}")
except OSError as e:
    print(f"Ошибка чтения слова: {e}")

# Запись нескольких байтов в регистр (например, [0x01, 0x02, 0x03] в 0x03)
try:
    i2c.write_bytes(device_addr, 0x03, [0x01, 0x02, 0x03])
    print("В регистр 0x03 записаны байты: [0x01, 0x02, 0x03]")
except OSError as e:
    print(f"Ошибка записи байтов: {e}")

# Чтение нескольких байтов из регистра (например, 3 байта из 0x03)
try:
    bytes_data = i2c.read_bytes(device_addr, 0x03, 3)
    print(f"Байты, прочитанные из регистра 0x03: {[hex(b) for b in bytes_data]}")
except OSError as e:
    print(f"Ошибка чтения байтов: {e}")

# Прямая запись данных без регистра (например, [0xAA, 0xBB] на устройство)
try:
    i2c.write_direct(device_addr, [0xAA, 0xBB])
    print("На устройство напрямую записаны байты: [0xAA, 0xBB]")
except OSError as e:
    print(f"Ошибка прямой записи: {e}")

# Прямое чтение данных с устройства без регистра (например, 2 байта)
try:
    direct_data = i2c.read_direct(device_addr, 2)
    print(f"Байты, прочитанные напрямую с устройства: {[hex(b) for b in direct_data]}")
except OSError as e:
    print(f"Ошибка прямого чтения: {e}")