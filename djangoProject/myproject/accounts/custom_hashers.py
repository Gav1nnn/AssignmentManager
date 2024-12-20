# accounts/custom_hashers.py

import hashlib
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
import secrets
from django.utils.crypto import get_random_string

class SHA256PasswordHasher(BasePasswordHasher):
    """
    The SHA256 password hasher.
    """
    algorithm = "sha256"

    def encode(self, password, salt):
        assert password is not None
        hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        if algorithm != self.algorithm:
            return False
        encoded_2 = self.encode(password, salt)
        return self.safe_compare(encoded, encoded_2)

    def safe_compare(self, a, b):
        return secrets.compare_digest(a, b)

    def harden_runtime(self, password, encoded):
        pass  # Do nothing - we don't want to waste CPU cycles on SHA-256

    def must_update(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        return algorithm != self.algorithm

    def salt(self):
        return get_random_string(12)  # 你可以根据需要调整盐的长度