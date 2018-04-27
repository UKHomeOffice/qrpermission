import pyqrcode
from skimage.io import imread as read_image
from unittest import TestCase
import zbar
import zbar.misc
from permission.permission import Permission, from_qr_code_format

PRIVATE_KEY = 'etc/permissions_key'
PUBLIC_KEY = 'etc/permissions_key.pub'
SCALE = 2

class TestScanning(TestCase):

    def should_have_valid_signature(self):
        perm = Permission('Joe Bloggs', '23/4/2015', 'NZ1234')
        perm.sign(PRIVATE_KEY)

        code = pyqrcode.create(perm.format_for_qr_code())
        code.png('permission.png', scale=SCALE)
        self.assertTrue(perm.check_signature(PUBLIC_KEY))

    def should_not_have_valid_signature(self):
        perm = Permission('Joe Bloggs', '23/4/2015', 'NZ1234')
        perm.sign(PRIVATE_KEY)
        perm.name = 'Fred Dagg'

        code = pyqrcode.create(perm.format_for_qr_code())
        code.png('forged.png', scale=SCALE)
        self.assertFalse(perm.check_signature(PUBLIC_KEY))

def __scan_barcode(image_filename):
    scanner = zbar.Scanner()
    image_as_numpy_array = __imread(image_filename)
    results = scanner.scan(image_as_numpy_array)
    if not results:
        return None
    for result in results:
        return from_qr_code_format(result.data.decode('ascii'))

def __imread(image_filename):
    image = read_image(image_filename)
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    return image
