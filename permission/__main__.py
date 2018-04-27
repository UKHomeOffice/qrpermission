import pyqrcode
from skimage.io import imread as read_image
import zbar
import zbar.misc
from permission.permission import Permission, from_qr_code_format

PRIVATE_KEY = 'etc/permissions_key'
PUBLIC_KEY = 'etc/permissions_key.pub'
SCALE = 2

def generate_qr_codes():
    perm = Permission('Joe Bloggs', '23/4/2015', 'NZ1234')
    perm.sign(PRIVATE_KEY)

    code = pyqrcode.create(perm.format_for_qr_code())
    code.png('permission.png', scale=SCALE)

    perm = Permission('Joe Bloggs', '23/4/2015', 'NZ1234')
    perm.signature = 'ABCDEFGH'

    code = pyqrcode.create(perm.format_for_qr_code())
    code.png('bad_signature.png', scale=SCALE)

    perm = Permission('Joe Bloggs', '23/4/2015', 'NZ1234')
    perm.sign(PRIVATE_KEY)
    perm.name = 'Fred Dagg'

    code = pyqrcode.create(perm.format_for_qr_code())
    code.png('forged.png', scale=SCALE)

def imread(image_filename):
    image = read_image(image_filename)
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    return image

def scan_barcode(image_filename):
    scanner = zbar.Scanner()
    print('scanning image ' + image_filename)
    image_as_numpy_array = imread(image_filename)
    results = scanner.scan(image_as_numpy_array)
    if not results:
        print('  No barcode found.')
    for result in results:
        # zbar returns barcode data as byte array, so decode byte array as ascii
        print('  type: {}, quality: {}'.format(result.type, result.quality))
        return from_qr_code_format(result.data.decode('ascii'))

def check_valid(permission):
    is_valid = permission.check_signature(PUBLIC_KEY)
    if is_valid:
        print("+++ Signature valid")
    else:
        print("--- Signature not valid")

generate_qr_codes()
check_valid(scan_barcode('permission.png'))
check_valid(scan_barcode('bad_signature.png'))
check_valid(scan_barcode('forged.png'))
