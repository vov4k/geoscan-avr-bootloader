import sys
import errno
import argparse
import fcntl
import os
from smbus2 import SMBus
from time import sleep

FIRMWARE_UPDATE_COMMAND = 0xAA

NOT_INTEL_HEX = 101
MALFORMATED = 102
CHECKSUM_FAILED = 103
PAGE_FULL = 201
WRONG_PAGE = 202
ILLEGAL_OPERATION = 203


def open_i2c(filename):
    try:
        file = os.open(filename, os.O_RDWR)
    except OSError:
        sys.stderr.write(f"[Error] Could not open {filename}\n")
        sys.exit(1)
    print(f"[OK] Opened I2C Interface on {filename}")
    return file


def send_enter_upgrade_command(device_handle):
    try:
        with SMBus(1) as bus:
            bus.write_byte(0x00, FIRMWARE_UPDATE_COMMAND)
    except IOError:
        sys.stderr.write("[Error] Failed to send firmware upgrade command\n")
        sys.exit(1)
    print("[OK] Sent firmware upgrade command. Nodes are now awaiting hex")


def send_data(device_handle, address, data, size):
    try:
        fcntl.ioctl(device_handle, 0x0703, address)
        os.write(device_handle, data)
    except OSError:
        sys.stderr.write(f"[Error] Failed to send data to address {address}\n")
        sys.exit(1)
    print("[OK] Data sent successfully")


def open_file(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        sys.stderr.write(f"Could not open the file {filename}\n")
        sys.exit(errno.ENOENT)
    return file


def upload_hex(file_handle, device_handle, address):
    i = 0
    for line in file_handle:
        if len(line) <= 2:  # Skip (almost) empty lines
            continue
        print(f"[Info] Sending line {i}")
        line = line.strip() + "\r\n"
        send_data(device_handle, address, line.encode(), len(line))
        print("[Info] Trying to get response")
        # Wait for target to re-enable i2c (do the flashing)
        while True:
            try:
                result = os.read(device_handle, 1)
                if result:
                    result = int.from_bytes(result, byteorder="big")
                    break
            except OSError:
                pass
        if result:
            error_message = {
                NOT_INTEL_HEX: "[Error] The data is not in Intel Hex Format\n",
                MALFORMATED: "[Error] The data is Malformed\n",
                CHECKSUM_FAILED: "[Warning] CHECKSUM FAILED! Retrying\n",
                PAGE_FULL: "[Error] The provided data does not fit Layout (Page Full)\n",
                WRONG_PAGE: "[Error] The data was not provided in the right order\n",
                ILLEGAL_OPERATION: "[Error] Other than 00 or 01 record type\n",
            }.get(result, "[Error] Unknown error occurred during upload\n")
            sys.stderr.write(error_message)
            sys.exit(1)
        i += 1


def reset_by_i2c(device_handle):
    with SMBus(1) as bus:
        bus.write_byte_data(0x27, 0x15, 42)


def main():
    parser = argparse.ArgumentParser(description="Atmega328p I2C bootloader utility")
    parser.add_argument("-e", action="store_true", help="Enter upgrade mode")
    parser.add_argument(
        "-d",
        metavar="DEVICE_PATH",
        type=str,
        default="/dev/i2c-1",
        help="Path to I2C device (default: /dev/i2c-1)",
    )
    parser.add_argument(
        "-a",
        metavar="ADDRESS",
        type=str,
        default="0x52",
        help="Address in hex for single upgrade (default: 0x52)",
    )
    parser.add_argument("-f", metavar="FILE_PATH", type=str, help="Path to hex file")
    parser.add_argument(
        "-r",
        action="store_true",
        help="Write value 42 to cell 0x15 at I2C address 0x27",
    )
    parser.add_argument(
        "-u",
        action="store_true",
        help="Perform full upgrade (Write value 42 to cell 0x15, Enter upgrade mode, Upload file)",
    )

    args = parser.parse_args()

    mode = None

    if args.u:
        mode = "FULL_UPGRADE"
    elif args.e:
        mode = "ENTER_UPGRADE"
    elif args.r:
        mode = "WRITE_CELL"
    elif args.f:
        mode = "UPGRADE_SINGLE"

    if mode == "ENTER_UPGRADE":
        device_handle = open_i2c(args.d)
        send_enter_upgrade_command(device_handle)
    elif mode == "UPGRADE_SINGLE":
        device_handle = open_i2c(args.d)
        file_handle = open_file(args.f)
        upload_hex(file_handle, device_handle, int(args.a, 16))
    elif mode == "WRITE_CELL":
        device_handle = open_i2c(args.d)
        reset_by_i2c(device_handle)
    elif mode == "FULL_UPGRADE":
        device_handle = open_i2c(args.d)
        reset_by_i2c(device_handle)
        sleep(0.5)
        send_enter_upgrade_command(device_handle)
        sleep(0.5)
        if args.f:
            file_handle = open_file(args.f)
            upload_hex(file_handle, device_handle, int(args.a, 16))
    else:
        parser.print_help()

    if "file_handle" in locals():
        file_handle.close()

    os.close(device_handle)


if __name__ == "__main__":
    main()
