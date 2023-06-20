import usb.core
import usb.util
import sys
import signal
import time


def main(vid, pid):
    device = usb.core.find(idVendor=vid, idProduct=pid)

    def handle_interrupt(signal, frame):
        print("Cleaning up...")
        usb.util.release_interface(device, 0)
        usb.util.dispose_resources(device)

    if not device:
        raise ValueError("Device not found!")

    interface_number = getInterface(device)
    # See FAQ about running libusb apps in MacOSX
    if device.is_kernel_driver_active(interface_number):
        try:
            device.detach_kernel_driver(interface_number)
        except usb.core.USBError as e:
            sys.exit(e)

    usb.util.claim_interface(device, 0)
    signal.signal(signal.SIGINT, handle_interrupt)

    endpoint_address = getEndpoint()
    report_size = getSize()
    while True:
        data = device.read(endpoint_address, report_size, 100)
        displayData(data)
        time.sleep(0.3)


def getInterface(device):
    print("Implement")


def getEndpoint(device):
    print("Implement")


def getSize(device):
    print("Implement")


def displayData(data):
    print("Implement")


def search():
    print("Searching for HIDs...")
    devices = list(usb.core.find(find_all=True))
    if not devices:
        print("No HIDs found!")

    text = " HID List "
    print(text.center(50, "="))
    for count, device in enumerate(devices):
        name = usb.util.get_string(device, 1) + " " + \
            usb.util.get_string(device, 2)
        vid = device.idVendor
        pid = device.idProduct
        print("[%d]>\n name: %s\n idVendor: %s\n idProduct: %s" %
            (count, name, hex(vid), hex(pid)))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hidr.py <vendor_id> <product_id>")
        search()
    else:
        idVendor = sys.argv[1]
        idProduct = sys.argv[2]
        main(int(idVendor, 16), int(idProduct, 16))
