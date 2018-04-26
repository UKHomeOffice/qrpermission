""" Data class which represents a digital permission"""
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class Permission:
    def __init__(self, name, expiry, passport):
        self.name = name
        self.expiry = expiry
        self.passport = passport
        self.signature = None

    def sign(self, key_file):
        with open(key_file, "r") as key:
            rsakey = RSA.importKey(key.read())
            signer = PKCS1_v1_5.new(rsakey)
            digest = SHA256.new()
            digest.update(self.name.encode('utf-8'))
            digest.update(self.passport.encode('utf-8'))
            digest.update(self.expiry.encode('utf-8'))
            sign = signer.sign(digest)
            self.signature = b64encode(sign).decode('ascii')

    def check_signature(self, key_file):
        with open(key_file, "r") as key:
            rsakey = RSA.importKey(key.read())
            signer = PKCS1_v1_5.new(rsakey)
            digest = SHA256.new()
            digest.update(self.name.encode('utf-8'))
            digest.update(self.passport.encode('utf-8'))
            digest.update(self.expiry.encode('utf-8'))
            return signer.verify(digest, b64decode(self.signature))

    def format_for_qr_code(self):
        return self.name + '\n' + \
               self.expiry + '\n' + \
               self.passport + '\n' + \
               self.signature

def from_qr_code_format(qr_code_text):
    lines = qr_code_text.split('\n')
    perm = Permission(lines[0], lines[1], lines[2])
    perm.signature = lines[3]
    return perm
