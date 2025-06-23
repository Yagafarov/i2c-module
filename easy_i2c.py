import machine

class EasyI2C:
    """
    Класс для упрощения работы с I2C на ESP32 с использованием MicroPython.
    Предоставляет методы для чтения и записи данных в регистры I2C устройств,
    а также для прямой записи и чтения без указания регистра.
    """

    def __init__(self, scl, sda, freq=100000):
        """
        Инициализация I2C шины.

        :param scl: Объект machine.Pin для SCL (серийные часы).
        :param sda: Объект machine.Pin для SDA (серийные данные).
        :param freq: Частота I2C шины (по умолчанию 100000 Гц).
        """
        if not isinstance(scl, machine.Pin) or not isinstance(sda, machine.Pin):
            raise ValueError("scl и sda должны быть объектами machine.Pin")
        self.i2c = machine.I2C(scl=scl, sda=sda, freq=freq)

    def scan(self, verbose=True):
        """
        Сканирование I2C шины для обнаружения подключенных устройств.

        :param verbose: Если True, выводит информацию о найденных устройствах.
        :return: Список адресов обнаруженных устройств.
        """
        devices = self.i2c.scan()
        if verbose:
            if devices:
                print("Обнаружены устройства I2C:")
                for addr in devices:
                    print(f" - Адрес: 0x{addr:02X}")
            else:
                print("Устройства не найдены.")
        return devices

    def _check_addr(self, device_addr):
        """Проверка допустимости адреса устройства."""
        if not 0 <= device_addr <= 127:
            raise ValueError("Адрес устройства должен быть в диапазоне 0-127")

    def write_byte(self, device_addr, reg_addr, value):
        """
        Запись одного байта в регистр устройства.

        :param device_addr: Адрес I2C устройства (0-127).
        :param reg_addr: Адрес регистра (обычно 0-255).
        :param value: Значение для записи (0-255).
        """
        self._check_addr(device_addr)
        if not 0 <= value <= 255:
            raise ValueError("Значение должно быть в диапазоне 0-255")
        try:
            self.i2c.writeto_mem(device_addr, reg_addr, bytes([value]))
        except OSError as e:
            print(f"Ошибка: Не удалось записать байт в устройство 0x{device_addr:02X}, регистр 0x{reg_addr:02X}")
            raise

    def read_byte(self, device_addr, reg_addr):
        """
        Чтение одного байта из регистра устройства.

        :param device_addr: Адрес I2C устройства (0-127).
        :param reg_addr: Адрес регистра (обычно 0-255).
        :return: Прочитанное значение (0-255).
        """
        self._check_addr(device_addr)
        try:
            return self.i2c.readfrom_mem(device_addr, reg_addr, 1)[0]
        except OSError as e:
            print(f"Ошибка: Не удалось прочитать байт из устройства 0x{device_addr:02X}, регистр 0x{reg_addr:02X}")
            raise

    def write_word(self, device_addr, reg_addr, value, byteorder='big'):
        """
        Запись 16-битного слова в регистр устройства.

        :param device_addr: Адрес I2C устройства (0-127).
        :param reg_addr: Адрес регистра (обычно 0-255).
        :param value: Значение для записи (0-65535).
        :param byteorder: Порядок байтов ('big' или 'little').
        """
        self._check_addr(device_addr)
        if not 0 <= value <= 65535:
            raise ValueError("Значение должно быть в диапазоне 0-65535")
        if byteorder == 'big':
            data = [(value >> 8) & 0xFF, value & 0xFF]
        else:
            data = [value & 0xFF, (value >> 8) & 0xFF]
        try:
            self.i2c.writeto_mem(device_addr, reg_addr, bytes(data))
        except OSError as e:
            print(f"Ошибка: Не удалось записать слово в устройство 0x{device_addr:02X}, регистр 0x{reg_addr:02X}")
            raise

    def read_word(self, device_addr, reg_addr, byteorder='big'):
        """
        Чтение 16-битного слова из регистра устройства.

        :param device_addr: Адрес I2C устройства (0-127).
        :param reg_addr: Адрес регистра (обычно 0-255).
        :param byteorder: Порядок байтов ('big' или 'little').
        :return: Прочитанное значение (0-65535).
        """
        self._check_addr(device_addr)
        try:
            data = self.i2c.readfrom_mem(device_addr, reg_addr, 2)
            if byteorder == 'big':
                return (data[0] << 8) | data[1]
            else:
                return (data[1] << 8) | data[0]
        except OSError as e:
            print(f"Ошибка: Не удалось прочитать слово из устройства 0x{device_addr:02X}, регистр 0x{reg_addr:02X}")
            raise

    def write_bytes(self, device_addr, reg_addr, data):
        """
        Запись нескольких байтов в регистр устройства.

        :param device_addr: Адрес I2C устройства (0-127).
        :param reg_addr: Адрес регистра (обычно 0-255).
        :param data: Байты для записи (bytes или list).
        """
        self._check_addr(device_addr)
        if isinstance(data, list):
            data = bytes(data)
        elif not isinstance(data, bytes):
            raise ValueError("data должен быть bytes или list")
        try:
            self.i2c.writeto_mem(device_addr, reg_addr, data)
        except OSError as e:
            print(f"Ошибка: Не удалось записать байты в устройство 0x{device_addr:02X}, регистр 0x{reg_addr:02X}")
            raise

    def read_bytes(self, device_addr, reg_addr, nbytes):
        """
        Чтение нескольких байтов из регистра устройства.

        :param device_addr: Адрес I2C устройства (0-127).
        :param reg_addr: Адрес регистра (обычно 0-255).
        :param nbytes: Количество байтов для чтения.
        :return: Прочитанные байты (bytes).
        """
        self._check_addr(device_addr)
        try:
            return self.i2c.readfrom_mem(device_addr, reg_addr, nbytes)
        except OSError as e:
            print(f"Ошибка: Не удалось прочитать байты из устройства 0x{device_addr:02X}, регистр 0x{reg_addr:02X}")
            raise

    def write_direct(self, device_addr, data):
        """
        Прямая запись данных на устройство без указания регистра.

        :param device_addr: Адрес I2C устройства (0-127).
        :param data: Данные для записи (bytes или list).
        """
        self._check_addr(device_addr)
        if isinstance(data, list):
            data = bytes(data)
        elif not isinstance(data, bytes):
            raise ValueError("data должен быть bytes или list")
        try:
            self.i2c.writeto(device_addr, data)
        except OSError as e:
            print(f"Ошибка: Не удалось записать данные на устройство 0x{device_addr:02X}")
            raise

    def read_direct(self, device_addr, nbytes):
        """
        Прямое чтение данных с устройства без указания регистра.

        :param device_addr: Адрес I2C устройства (0-127).
        :param nbytes: Количество байтов для чтения.
        :return: Прочитанные байты (bytes).
        """
        self._check_addr(device_addr)
        try:
            return self.i2c.readfrom(device_addr, nbytes)
        except OSError as e:
            print(f"Ошибка: Не удалось прочитать данные с устройства 0x{device_addr:02X}")
            raise