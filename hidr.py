import usb.core
import usb.util
import sys
import signal

def main(vid, pid):
    device = usb.core.find(idVendor=vid, idProduct=pid)
    if not device:
        raise ValueError("Device not found!")
    usb.util.claim_interface(device, 0)
    signal.signal(signal.SIGINT, handle_interrupt)

    endpoint_address = 0x81
    report_size = 8
    timeout = 1000
    while True:
        data = device.read(endpoint_address, report_size, timeout)
        print(data)

def handle_interrupt(signal, frame, device):
    print("Cleaning up...")
    usb.util.release_interface(device, 0)
    usb.util.dispose_resources(device)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hidr.py <vendor_id> <product_id>")
    else:
        idVendor = sys.argv[1]
        idProduct = sys.argv[2]
        main(idVendor, idProduct)