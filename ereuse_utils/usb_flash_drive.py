import inflection as inflection
import usb.core
import usb.util

from usb import CLASS_MASS_STORAGE


def plugged_usbs():
    # type: () -> map
    """Gets the plugged-in USB Flash drives (pen-drives)."""

    class FindPenDrives(object):
        # From https://github.com/py9usb/pyusb/blob/master/docs/tutorial.rst
        def __init__(self, class_):
            self._class = class_

        def __call__(self, device):
            # first, let's check the device
            if device.bDeviceClass == self._class:
                return True
            # ok, transverse all devices to find an
            # interface that matches our class
            for cfg in device:
                # find_descriptor: what's it?
                intf = usb.util.find_descriptor(
                    cfg,
                    bInterfaceClass=self._class
                )
                if intf is not None:
                    return True

            return False

    def get_pendrive(pen):
        # type: (usb.Device) -> dict
        manufacturer = pen.manufacturer.strip()
        model = pen.product.strip()
        serial_number = pen.serial_number.strip()
        hid = manufacturer + '-' + model + '-' + inflection.parameterize(serial_number, '_')
        return {
            '_id': hid,  # Make live easier to DeviceHubClient by using _id
            'hid': hid,
            '@type': 'USBFlashDrive',
            'serialNumber': serial_number,
            'model': model,
            'manufacturer': manufacturer,
            'vendorId': pen.idVendor,
            'productId': pen.idProduct
        }

    return map(get_pendrive, usb.core.find(find_all=True, custom_match=FindPenDrives(CLASS_MASS_STORAGE)))
