import os
import json
import base64
import time
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")

class OpenClawMemory:
    def __init__(self, master_key: Optional[str] = None):
        self.key = self._derive_key(master_key or "openclaw_default_unsecure_key_123")
        self.is_encrypted_properly = master_key is not None
        self.memory_data = {}
        self.load_memory()

    def _derive_key(self, master_key: str) -> bytes:
        """Derives a 32-byte key from the master key."""
        salt = b'openclaw_default_salt_32'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(master_key.encode())

    def _encrypt(self, data: str) -> str:
        """Encrypts data using AES-256-CBC."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext).decode()

    def _decrypt(self, encrypted_data: str) -> str:
        """Decrypts data using AES-256-CBC."""
        raw_data = base64.b64decode(encrypted_data)
        iv = raw_data[:16]
        ciphertext = raw_data[16:]
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode()

    def load_memory(self):
        """Loads and decrypts memory from disk."""
        if not os.path.exists(MEMORY_FILE):
            self.memory_data = {"facts": {}, "history": [], "reminders": []}
            return

        try:
            with open(MEMORY_FILE, "r") as f:
                encrypted_str = f.read()
                if not encrypted_str:
                    self.memory_data = {"facts": {}, "history": [], "reminders": []}
                    return
                decrypted_json = self._decrypt(encrypted_str)
                self.memory_data = json.loads(decrypted_json)
                self._clean_expired_entries()
        except Exception as e:
            print(f"🔴 Memory Error: Could not load memory ({e}). Check master key.")
            self.memory_data = {"facts": {}, "history": [], "reminders": []}

    def save_memory(self):
        """Encrypts and saves memory to disk."""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            
        json_data = json.dumps(self.memory_data)
        encrypted_str = self._encrypt(json_data)
        with open(MEMORY_FILE, "w") as f:
            f.write(encrypted_str)

    def remember(self, key: str, value: any, permanent: bool = False):
        """Stores a fact with an expiry timestamp."""
        expiry = None if permanent else (datetime.now() + timedelta(days=90)).timestamp()
        self.memory_data["facts"][key] = {
            "value": value,
            "expiry": expiry,
            "recorded_at": datetime.now().isoformat()
        }
        self.save_memory()

    def forget(self, key: str):
        """Removes a fact from memory."""
        if key in self.memory_data["facts"]:
            del self.memory_data["facts"][key]
            self.save_memory()

    def _clean_expired_entries(self):
        """Removes entries older than 90 days."""
        now = datetime.now().timestamp()
        to_delete = []
        for key, entry in self.memory_data.get("facts", {}).items():
            if entry.get("expiry") and now > entry["expiry"]:
                to_delete.append(key)
        
        for key in to_delete:
            del self.memory_data["facts"][key]
        
        if to_delete:
            self.save_memory()

    def get_fact(self, key: str, default=None):
        return self.memory_data.get("facts", {}).get(key, {}).get("value", default)
