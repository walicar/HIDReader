import usb.core
import usb.util
import sys
import signal
import time


def main(vid, pid):
    device = usb.core.find(idVendor=vid, idProduct=pid)
    print(device)
    print("\n")

    def handle_interrupt(signal, frame):
        print("Cleaning up...")
        usb.util.release_interface(device, 0)
        usb.util.dispose_resources(device)
        sys.exit(0)

    if not device:
        raise ValueError("Device not found!")

    interface_number = findHID(device)
    # See FAQ about running libusb apps in MacOSX
    if device.is_kernel_driver_active(interface_number):
        try:
            device.detach_kernel_driver(interface_number)
        except usb.core.USBError as e:
            sys.exit(e)

    usb.util.claim_interface(device, 0)
    signal.signal(signal.SIGINT, handle_interrupt)

    endpoint_address = 0x84
    report_size = getSize(device, interface_number)
    text = " INPUT "
    print(text.center(50, "="))
    while True:
        data = device.read(endpoint_address, report_size, 100)
        displayData(data)
        time.sleep(0.3)


def findHID(device):
    for cfg in device:
        intf = usb.util.find_descriptor(cfg, bInterfaceClass=0x3)
        if intf is not None:
            return intf.bInterfaceNumber
    return -1


def getSize(device, interface_number):
    intf = None
    for cfg in device:
        intf = usb.util.find_descriptor(cfg, bInterfaceNumber=interface_number)
        if intf is not None:
            break
    ep = usb.util.find_descriptor(intf, bEndpointAddress=0x84)
    if ep is not None:
        return ep.wMaxPacketSize
    return -1

def displayData(data):
    entry_width = len(str(len(data)))
    for count, byte in enumerate(data):
        print(f"[{count:>{entry_width}}]: ", end="")
        if (count + 1) % 4 == 0:
            print(f"{byte:>{4}}")
        else:
            print(f"{byte:>{4}}", end =", ")
    print("\n")
    time.sleep(0.2)


def search():
    print("Searching for HIDs...")
    devices = list(usb.core.find(find_all=True))
    hids = [device for device in devices if findHID(device) != -1]

    if not hids:
        print("No HIDs found!")

    text = " HID List "
    print(text.center(50, "="))
    for count, device in enumerate(hids):
        vid = device.idVendor
        pid = device.idProduct
        name = usb.util.get_string(device, 1) + " " + \
            usb.util.get_string(device, 2)
        print("[%d]>\n name: %s\n idVendor: %s\n idProduct: %s" %
              (count, name, hex(vid), hex(pid)))
        print("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hidr.py <vendor_id> <product_id>")
        search()
    else:
        idVendor = sys.argv[1]
        idProduct = sys.argv[2]
        main(int(idVendor, 16), int(idProduct, 16))
