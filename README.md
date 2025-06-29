# EasyI2C - Библиотека для работы с I2C в MicroPython

`EasyI2C` - это удобная библиотека для работы с I2C-устройствами на микроконтроллерах (например, ESP32 или Raspberry Pi Pico) с использованием MicroPython. Она упрощает операции чтения и записи данных в регистры устройств, предоставляя интуитивно понятный интерфейс, обработку ошибок и гибкость в работе с различными форматами данных.

## Основные возможности

- **Простота использования**: Методы для записи и чтения байтов, слов (16-бит) и массивов байтов.
- **Обработка ошибок**: Автоматический перехват и информативные сообщения об ошибках.
- **Проверка входных данных**: Проверка адресов устройств, регистров и значений.
- **Гибкость байтового порядка**: Поддержка `big-endian` и `little-endian` для 16-битных слов.
- **Сканирование устройств**: Удобный вывод адресов подключенных I2C-устройств.
- **Прямые операции**: Поддержка записи и чтения без указания регистра.
- **Документация**: Подробные комментарии на русском языке для всех методов.

## Требования

- Микроконтроллер с поддержкой MicroPython (например, ESP32, ESP8266, Raspberry Pi Pico).
- MicroPython версии 1.18 или выше.
- I2C-устройство, подключенное к микроконтроллеру (например, датчик, дисплей).

## Установка

1. Скачайте файл `easy_i2c.py` из репозитория.
2. Скопируйте файл `easy_i2c.py` в файловую систему вашего микроконтроллера (например, используя Thonny или `ampy`).
3. Подключите I2C-устройство к микроконтроллеру:
   - SCL → выбранный пин (например, пин 22).
   - SDA → выбранный пин (например, пин 21).
   - Убедитесь, что используются подтягивающие резисторы (обычно 4.7 кОм), если они не встроены в устройство.

## Использование

### Инициализация

Создайте экземпляр класса `EasyI2C`, указав пины SCL и SDA, а также частоту шины (по умолчанию 100 кГц):

```python
from machine import Pin
from easy_i2c import EasyI2C

i2c = EasyI2C(scl=Pin(22), sda=Pin(21), freq=100000)
```

### Основные методы

| Метод | Описание | Параметры |
|-------|----------|-----------|
| `scan(verbose=True)` | Сканирует шину I2C и возвращает список адресов устройств. Если `verbose=True`, выводит результаты в консоль. | `verbose`: Булевый флаг для вывода информации. |
| `write_byte(device_addr, reg_addr, value)` | Записывает один байт в регистр устройства. | `device_addr`: Адрес устройства (0-127).<br>`reg_addr`: Адрес регистра (обычно 0-255).<br>`value`: Значение (0-255). |
| `read_byte(device_addr, reg_addr)` | Читает один байт из регистра устройства. | `device_addr`, `reg_addr`: Как выше. |
| `write_word(device_addr, reg_addr, value, byteorder='big')` | Записывает 16-битное слово в регистр. | `device_addr`, `reg_addr`, `value`: Значение (0-65535).<br>`byteorder`: `'big'` или `'little'`. |
| `read_word(device_addr, reg_addr, byteorder='big')` | Читает 16-битное слово из регистра. | Как выше. |
| `write_bytes(device_addr, reg_addr, data)` | Записывает массив байтов в регистр. | `device_addr`, `reg_addr`, `data`: `bytes` или `list`. |
| `read_bytes(device_addr, reg_addr, nbytes)` | Читает указанное количество байтов из регистра. | `device_addr`, `reg_addr`, `nbytes`: Количество байтов. |
| `write_direct(device_addr, data)` | Прямая запись данных без регистра. | `device_addr`, `data`: `bytes` или `list`. |
| `read_direct(device_addr, nbytes)` | Прямое чтение данных без регистра. | `device_addr`, `nbytes`. |

### Пример кода

```python
from machine import Pin
from easy_i2c import EasyI2C

# Инициализация I2C
i2c = EasyI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# Сканирование устройств
print("Результаты сканирования I2С:")
devices = i2c.scan(verbose=True)

# Если устройство найдено, используем его адрес
if devices:
    device_addr = devices[0]
else:
    print("Ошибка: Устройства не найдены!")
    exit()

# Запись и чтение одного байта
try:
    i2c.write_byte(device_addr, 0x01, 0xFF)
    print("В регистр 0x01 записан байт 0xFF")
    value = i2c.read_byte(device_addr, 0x01)
    print(f"Байт из регистра 0x01: 0x{value:02X}")
except OSError as e:
    print(f"Ошибка: {e}")

# Запись и чтение 16-битного слова
try:
    i2c.write_word(device_addr, 0x02, 0x1234, byteorder='big')
    print("В регистр 0x02 записано слово 0x1234")
    word = i2c.read_word(device_addr, 0x02, byteorder='big')
    print(f"Слово из регистра 0x02: 0x{word:04X}")
except OSError as e:
    print(f"Ошибка: {e}")

# Запись и чтение нескольких байтов
try:
    i2c.write_bytes(device_addr, 0x03, [0x01, 0x02, 0x03])
    print("В регистр 0x03 записаны байты: [0x01, 0x02, 0x03]")
    bytes_data = i2c.read_bytes(device_addr, 0x03, 3)
    print(f"Байты из регистра 0x03: {[hex(b) for b in bytes_data]}")
except OSError as e:
    print(f"Ошибка: {e}")

# Прямая запись и чтение
try:
    i2c.write_direct(device_addr, [0xAA, 0xBB])
    print("На устройство записаны байты: [0xAA, 0xBB]")
    direct_data = i2c.read_direct(device_addr, 2)
    print(f"Байты, прочитанные напрямую: {[hex(b) for b in direct_data]}")
except OSError as e:
    print(f"Ошибка: {e}")
```

## Обработка ошибок

Библиотека автоматически перехватывает ошибки `OSError`, возникающие при недоступности устройства или некорректных операциях, и выводит информативные сообщения. Например:
```
Ошибка: Не удалось записать байт в устройство 0x40, регистр 0x01
```

Также проверяются входные параметры:
- Адрес устройства (0-127).
- Значение байта (0-255).
- Значение слова (0-65535).
- Тип данных для массивов (`bytes` или `list`).

## Преимущества перед `machine.I2C`

- **Упрощённый интерфейс**: Не нужно вручную обрабатывать форматы данных или байтовый порядок.
- **Автоматическая проверка**: Защита от некорректных входных данных.
- **Информативные ошибки**: Понятные сообщения для отладки.
- **Гибкость**: Поддержка операций с регистрами и без них, а также различных форматов данных.

## Ограничения

- Библиотека зависит от модуля `machine.I2C` в MicroPython.
- Требуется правильное подключение I2C-устройства с подтягивающими резисторами.
- Не поддерживает сложные протоколы I2C, требующие нестандартных операций.

---

*Последнее обновление: 23 июня 2025 г.*