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
    ### See FAQ about running libusb apps in MacOSX
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
    # basically list all HIDs
    # NAME, idVendor, idProduct
    print("Implement")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hidr.py <vendor_id> <product_id>")
        search()
    else:
        idVendor = sys.argv[1]
        idProduct = sys.argv[2]
        main(int(idVendor, 16), int(idProduct, 16))