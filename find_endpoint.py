import libusb_package
import usb.backend.libusb1
import usb.core

if __name__ == "__main__":
    libusb1_backend = usb.backend.libusb1.get_backend(
        find_library=libusb_package.find_library
    )
    # Find our device
    dev = usb.core.find(idVendor=0x1e0e, idProduct=0x902b, backend=libusb1_backend) #Fiuu
    # dev = usb.core.find(idVendor=0x0B00, idProduct=0x0055, backend=libusb1_backend)  #BCA

    if dev is None:
        raise ValueError('Device not found')
    
    # Get the active configuration
    config = dev.get_active_configuration()
    
    print(config)