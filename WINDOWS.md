# Загрузка bootloader на atmega328p и прошивка через него
## Подготовка
1. Установить драйвера для USBasp. Запустить `InstallDriver.exe` из папки USBasp-driver.
2. Установить [PuTTy](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.80-installer.msi).
3. Установить джампер на USBasp, как показано на фото.
![jumper.jpeg](img%2Fjumper.jpeg)
4. Подключить USBasp к плате робота **правильной** стороной (обратите внимание на расположение надписей "MISO", "SCK", "RST").
![connection.jpeg](img%2Fconnection.jpeg)

## Установка bootloader
1. Распаковать архив `geoscan-avr-bootloader-main`.
2. С зажатым shift нажать ПКМ на распакованную из архива папку `geoscan-avr-bootloader-main`.
![file_path.jpeg](img%2Ffile_path.jpeg)
3. В командной строке: 

```
cd скопированный_путь

avrdude -p m328p -c usbasp -P usb -U lfuse:w:0xFF:m -U hfuse:w:0xD8:m -U efuse:w:0xFF:m -B 32

avrdude -F -p m328p -c usbasp -P usb -U flash:w:bootloader.hex
```

![cmd_avrdude.jpeg](img%2Fcmd_avrdude.jpeg)

4. Отключить USBasp от платы.

## Установка прошивки

1. Подключить аккумулятор.
2. Подключить робота к компьютеру по ethernet.
3. Подключится к роботу по ssh через PuTTy:

```
Host Name: arena-rpi-geobot
Login: pi
Password: raspberry
```

![putty.jpg](img%2Fputty.jpg)

![ssh_first.jpeg](img%2Fssh_first.jpeg)

4. Перейти в каталог _firmware_:
```
cd firmware
```
5. Загрузить прошивку:

```
python upload_firmware.py -e
python upload_firmware.py -f firmware.hex
```
![ssh_second.jpeg](img%2Fssh_second.jpeg)
6. Для последующих обновлений достаточно подключится к роботу по ssh и выполнить следующие команды:

```
cd firmware
python upload_firmware.py -u -f path_to_new_firmware
```

