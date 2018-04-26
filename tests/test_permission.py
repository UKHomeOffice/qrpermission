from base64 import b64encode
from unittest import TestCase
from permission.permission import Permission, from_qr_code_format

class TestPermission(TestCase):

    def test_signature(self):
        perm = Permission("Mickey Mouse", "12/2/2018", "GB123456789")
        perm.sign("etc/permissions_key")
        self.assertTrue(perm.signature.startswith('T4M+qHTFTK7HZTaZPjfxzJijf/4C3h'))

    def test_verify(self):
        perm = Permission("Mickey Mouse", "12/2/2018", "GB123456789")
        perm.sign("etc/permissions_key")
        self.assertTrue(perm.check_signature("etc/permissions_key.pub"))

    def test_verify_invalid_sig(self):
        perm = Permission("Mickey Mouse", "12/2/2018", "GB123456789")
        perm.sign("etc/permissions_key")
        perm.signature = b64encode(b'Some other signature')
        self.assertFalse(perm.check_signature("etc/permissions_key.pub"))

    def test_verify_forged(self):
        perm = Permission("Mickey Mouse", "12/2/2018", "GB123456789")
        perm.sign("etc/permissions_key")
        perm.name = 'Donald Duck'
        self.assertFalse(perm.check_signature("etc/permissions_key.pub"))

    def test_format_for_qr(self):
        perm = Permission("Mickey Mouse", "12/2/2018", "GB123456789")
        perm.sign("etc/permissions_key")
        self.assertTrue(perm.format_for_qr_code()
                        .startswith('Mickey Mouse\n12/2/2018\nGB123456789\nT4M+'))

    def test_parse_from_qr(self):
        perm = from_qr_code_format('Donald Duck\n12/5/2011\nGB987654321\nSome Signature')
        self.assertEqual('Donald Duck', perm.name)
        self.assertEqual('12/5/2011', perm.expiry)
        self.assertEqual('GB987654321', perm.passport)
        self.assertEqual('Some Signature', perm.signature)
