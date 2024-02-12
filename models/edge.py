from datetime import datetime
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
            'encrypted_value': self.encrypted_value,
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

class edge_usuario_contrasenia:
    def __init__(self, origin_url, action_url, username_value, password_value, date_created, date_last_used):
        self.origin_url = origin_url
        self.action_url = action_url
        self.username_value = username_value
        self.password_value = password_value
        self.date_created = date_created
        self.date_last_used = date_last_used

    def to_dict(self):
        # Convierte las fechas al formato específico
        creation_utc_str = format_date(self.date_created)
        expires_utc_str = format_date(self.date_last_used)
        return {
            'origin_url': self.origin_url,
            'action_url': self.action_url,
            'username_value': self.username_value,
            'password_value': self.password_value,
            'date_created': creation_utc_str,
            'date_last_used': expires_utc_str
        }

