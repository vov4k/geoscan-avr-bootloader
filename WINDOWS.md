# Загрузка bootloader на atmega328p и прошивка через него
## Подготовка
1. Скачайте и распакуйте архив [geoscan-avr-bootloader-main](https://github.com/vov4k/geoscan-avr-bootloader/archive/refs/heads/main.zip). 
1. Установите драйвера для USBasp. Запустите `InstallDriver.exe` из папки `USBasp-driver` внутри `geoscan-avr-bootloader-main`.
2. Установите джампер на USBasp, как показано на фото.
![jumper.jpeg](img%2Fjumper.jpeg)
3. Подключите USBasp к плате робота **правильной** стороной (обратите внимание на расположение надписей "MISO", "SCK", "RST").
![connection.jpeg](img%2Fconnection.jpeg)

## Установка bootloader
1. С зажатым shift нажмите ПКМ на распакованную из архива папку `geoscan-avr-bootloader-main`.
![file_path.jpeg](img%2Ffile_path.jpeg)
2. В командной строке (для её открытия одновременно нажмите клавишу Windows и кнопку R. Наберите в строке cmd, а затем нажмите Enter): 

```
cd скопированный_путь
```
```
avrdude -p m328p -c usbasp -P usb -U lfuse:w:0xFF:m -U hfuse:w:0xD8:m -U efuse:w:0xFF:m -U flash:w:geobotavr_bootloader.hex -B 32
```

![cmd_avrdude.jpeg](img%2Fcmd_avrdude.jpeg)

3. Отключите USBasp от платы.

## Установка прошивки

1. Подключите аккумулятор.
2. Подключите робота к компьютеру по ethernet.
3. Подключитесь к роботу по ssh. В командной строке:
```
ssh pi@arena-rpi-geobot
```
Пароль: raspberry

![ssh_first.jpeg](img%2Fssh_first.jpeg)

4. Перейти в каталог _firmware_:
```
cd firmware
```
5. Загрузить прошивку:

```
python upload_firmware.py -e
```
```
python upload_firmware.py -f geobotavr_firmware.hex
```
![ssh_second.jpeg](img%2Fssh_second.jpeg)

