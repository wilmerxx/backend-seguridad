import base64
from datetime import datetime


class FirefoxCookie:
    def __init__(self, originAttributes, host, name, value, path, expiry, lastAccessed, isHttpOnly, isSecure):
        self.originAttributes = originAttributes
        self.name = name
        self.value = value
        self.path = path
        self.host = host
        self.expiry = expiry
        self.lastAccessed = lastAccessed
        self.isHttpOnly = isHttpOnly
        self.isSecure = isSecure

    def to_dict(self):
        # Verifica si 'expiry' y 'lastAccessed' son números antes de intentar convertirlos a un objeto datetime
        expiry_datetime = datetime.utcfromtimestamp(self.expiry) if self.expiry else None

        if isinstance(self.lastAccessed, (int, float)):
            try:
                # Convierte 'lastAccessed' de microsegundos a segundos antes de convertirlo a un objeto datetime
                last_accessed_datetime = datetime.utcfromtimestamp(self.lastAccessed / 1_000_000)
                date_str = last_accessed_datetime.strftime("%Y-%m-%d")
            except OSError:
                last_accessed_datetime = None
                date_str = None
        else:
            last_accessed_datetime = None
            date_str = None

        return {
            'originAttributes': self.originAttributes,
            'name': self.name,
            'value': self.value,
            'path': self.path,
            'host': self.host,
            'expiry': str(expiry_datetime),  # Convierte la fecha a una cadena para la representación JSON
            'lastAccessed': date_str,  # Incorpora date_str en el diccionario
            'isHttpOnly': self.isHttpOnly,
            'isSecure': self.isSecure,
        }

class EdgeCookie:
    def __init__(self, creation_utc, host_key, top_frame_site_key, name, value, path, expires_utc, is_secure,
                 is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port,
                 encrypted_value):
        self.creation_utc = creation_utc
        self.host_key = host_key
        self.top_frame_site_key = top_frame_site_key
        self.name = name
        self.value = value
        self.path = path
        self.expires_utc = expires_utc
        self.is_secure = is_secure
        self.is_httponly = is_httponly
        self.last_access_utc = last_access_utc
        self.has_expires = has_expires
        self.is_persistent = is_persistent
        self.priority = priority
        self.samesite = samesite
        self.source_port = source_port
        self.encrypted_value = encrypted_value

    def to_dict(self):
        # Convierte las fechas al formato específico de Firefox
        creation_utc_str = format_date(self.creation_utc)
        expires_utc_str = format_date(self.expires_utc)
        last_access_utc_str = format_date(self.last_access_utc)

        return {
            'creation_utc': creation_utc_str,
            'host_key': self.host_key,
            'top_frame_site_key': self.top_frame_site_key,
            'name': self.name,
            'value': self.value,
            'path': self.path,
            'expires_utc': expires_utc_str,
            'is_secure': self.is_secure,
            'is_httponly': self.is_httponly,
            'last_access_utc': last_access_utc_str,
            'has_expires': self.has_expires,
            'is_persistent': self.is_persistent,
            'priority': self.priority,
            'samesite': self.samesite,
            'source_port': self.source_port,
            'encrypted_value': base64.b64encode(self.encrypted_value).decode('utf-8') if self.encrypted_value else None,
        }


def format_date(timestamp):
    if isinstance(timestamp, (int, float)):
        try:
            # Convierte el timestamp a un objeto datetime y luego formatea como string
            date_obj = datetime.utcfromtimestamp(timestamp / 1_000_000)
            date_str = date_obj.strftime("%Y-%m-%d:::")[:-3]
        except OSError:
            date_str = None
    else:
        date_str = None

    return date_str


class FirefoxInterface:
    firefox_class = FirefoxCookie

    def open_session(self, app,request):
        #recuperar las cookies de session
        return self.firefox_class()

    def save_session(self, session, response):
        #guardar las cookies de session
        pass

