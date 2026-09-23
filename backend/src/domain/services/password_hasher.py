"""Hash de mots de passe via PBKDF2-HMAC-SHA256 (stdlib, aucune compilation)."""
import hashlib
import hmac
import secrets

ITERATIONS = 200_000
SALT_BYTES = 16
DIGEST = "sha256"
DIGEST_BYTES = 32


class PasswordHasher:
    def hash(self, password: str) -> str:
        salt = secrets.token_bytes(SALT_BYTES)
        derived = hashlib.pbkdf2_hmac(
            DIGEST, password.encode("utf-8"), salt, ITERATIONS, DIGEST_BYTES
        )
        return f"pbkdf2${DIGEST}${ITERATIONS}${salt.hex()}${derived.hex()}"

    def verify(self, password: str, stored: str) -> bool:
        try:
            scheme, digest, iters, salt_hex, hash_hex = stored.split("$")
        except ValueError:
            return False
        if scheme != "pbkdf2":
            return False
        try:
            iters_i = int(iters)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(hash_hex)
        except ValueError:
            return False
        computed = hashlib.pbkdf2_hmac(
            digest, password.encode("utf-8"), salt, iters_i, len(expected)
        )
        return hmac.compare_digest(computed, expected)
