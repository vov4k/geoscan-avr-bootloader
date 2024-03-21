BOOTSTART=0x7000
PART=m328p
MCU=atmega328p

PROG=usbasp

F_CPU=16000000

FLAGS=-I./include/ -mmcu=$(MCU) -DF_CPU=$(F_CPU)UL -Os -Wall -Wl,--section-start=.text=$(BOOTSTART)

LFUSE=0xFF
HFUSE=0xD8
EFUSE=0xFF

SRC= \
	main.c \
	src/hex_parse.c
HDR=

all: bootloader.hex

%.hex: %.elf
	avr-objcopy -j .text -j .data -O ihex $< $@

bootloader.elf: $(SRC) $(HDR)
	avr-gcc $(FLAGS) $(SRC) -o bootloader.elf

flash: bootloader.hex
	avrdude -F -p $(PART) -c $(PROG) -P usb -U flash:w:bootloader.hex

fuse:
	avrdude -p $(PART) -c $(PROG) -P usb -U lfuse:w:$(LFUSE):m -U hfuse:w:$(HFUSE):m -U efuse:w:$(EFUSE):m -B 32

clean:
	rm bootloader.hex bootloader.elf

disasm:
	avr-objdump -s -m avr5 -D bootloader.hex

reset:	# The v in the fuse parameters is for verify, might fail, but resets anyway.
	avrdude -p $(PART) -c $(PROG) -P usb -B 32  -Ulfuse:v:0xE1:m