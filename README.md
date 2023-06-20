# HIDReader

Easily monitor what HIDs are sending over USB using a simple python script.

Usecase: I wrote this script to figure out what data my PS4 Controller was sending.

## Requirements
- [libusb](https://formulae.brew.sh/formula/libusb)
- [pyusb](https://pypi.org/project/pyusb/)

## Usage

1. Connect your HID to your machine.
2. Run `sudo python3 hidr.py 0xffff 0xffff`

If you don't know what your HID's Vendor ID and Product ID are, you can simply run `python3 hidr.py`, and you will find a list of all HIDs connected to your machine, along with their respective Vendor IDs and Product IDs.

## Notes
- This script works on MacOSX and Linux, but has not been tested on Windows. 
- If you are encountering this error on Linux: `usb.core.USBError: [Errno 13] Access denied (insufficient permissions)`.
    - run `echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="ffff", ATTR{idProduct}=="ffff", MODE="0666"' >> /etc/udev/rules.d/10-local.rules`
    - Make sure to add the Vendor IDs and Product IDs where "ffff" are.
