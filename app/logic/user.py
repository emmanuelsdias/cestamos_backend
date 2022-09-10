import hashlib
import string
import secrets

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_token():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(20))