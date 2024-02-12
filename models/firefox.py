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

class FirefoxUsuarios:
    #aux = {"origin_url": origin_url,"action_url": action_url,"username_value": username_value,"password_value": password, "date_created": date_created, "date_last_used": date_last_used }
    def __init__(self, origin_url, action_url, username_value, password_value, date_created, date_last_used):
        self.origin_url = origin_url
        self.action_url = action_url
        self.username_value = username_value
        self.password_value = password_value
        self.date_created = date_created
        self.date_last_used = date_last_used

    def to_dict(self):

        date = datetime.utcfromtimestamp(self.date_created / 1_000_000)
        date_created = date.strftime("%Y-%m-%d")
        date_last = datetime.utcfromtimestamp(self.date_last_used / 1_000_000)
        date_last_used = date_last.strftime("%Y-%m-%d")
        return {
            'origin_url': self.origin_url,
            'action_url': self.action_url,
            'username_value': self.username_value,
            'password_value': self.password_value,
            'date_created': date_created,
            'date_last_used': date_last_used
        }
