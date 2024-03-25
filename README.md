# geoscan-avr-bootloader
Bootloader и python скрипт для загрузки прошивки на Atmega328P по I2C.
### Загрузчик (main.c)

#### Обзор
Загрузчик написан на основе https://github.com/ThomasDebrunner/millionboot

Загрузчик предназначен для приема обновлений прошивки по I2C. Он разбирает данные, отформатированные в формате Intel Hex, и записывает их во флэш-память с адреса 0x0000.

#### Конфигурация

- **Платформа:** Atmega328p
- **Размер Загрузчика:** 4KB
- **Команда Обновления Прошивки:** 0xAA

#### Инструкции
1. **Компиляция Загрузчика:** Запустите команду `make` для компиляции загрузчика.

2. **Прошивка Загрузчика:** Используйте команду `make flash` для прошивки скомпилированного загрузчика на микроконтроллер Atmega328p.

3. **Конфигурация Fuse:** Установите конфигурацию Fuse с помощью команды `make fuse`. Это обеспечивает правильную работу загрузчика.

4. **Очистка:** Для удаления сгенерированных файлов используйте `make clean`.

### Скрипт Загрузки Прошивки (main.py)

#### Зависимости

- `smbus2`: библиотека Python для взаимодействия с устройствами по I2C.

#### Использование

- `-e`: Ввести в режим обновления.
- `-d ПУТЬ_УСТРОЙСТВА`: Указать путь к устройству I2C (по умолчанию: `/dev/i2c-1`).
- `-a АДРЕС`: Указать адрес в шестнадцатеричном формате для одиночного обновления (по умолчанию: `0x52`).
- `-f ПУТЬ_ФАЙЛА`: Указать путь к файлу hex.
- `-r`: Перезагрузка. Записать значение 42 в ячейку 0x15 по адресу I2C 0x27.
- `-u`: Выполнить полное обновление (перезагрузить, войти в режим обновления, загрузить файл).

#### Пример
Для первой прошивки (после установки bootloader):
```
python upload_firmware.py -e
python upload_firmware.py -f firmware.hex
```

Для выполнения последующих обновлений:
```
python upload_firmware.py -u -f firmware.hex
```