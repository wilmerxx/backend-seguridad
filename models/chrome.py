from models.edge import format_date


class ChromeCookie:
    def __init__(self, creation_utc, host_key, top_frame_site_key, name, value, encrypted_value, path, expires_utc, is_secure, is_httponly, last_access_utc, has_expires, is_persistent, priority, samesite, source_port, last_update_utc):
        self.creation_utc = creation_utc
        self.host_key = host_key
        self.top_frame_site_key = top_frame_site_key
        self.name = name
        self.value = value
        self.encrypted_value = encrypted_value
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
        self.last_update_utc = last_update_utc

    def to_dict(self):
        # Convierte las fechas al formato específico de Firefox
        creation_utc_str = format_date(self.creation_utc)
        expires_utc_str = format_date(self.expires_utc)
        last_access_utc_str = format_date(self.last_access_utc)
        last_update_utc_str = format_date(self.last_update_utc)

        return {
            'creation_utc': creation_utc_str,
            'host_key': self.host_key,
            'top_frame_site_key': self.top_frame_site_key,
            'name': self.name,
            'value': self.value,
            'encrypted_value': self.encrypted_value,
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
            'last_update_utc': last_update_utc_str,
        }

class ChromeUser:

    def __init__(self, origin_url, username_value, password_value, signon_realm, date_created, date_last_used, date_password_modified):
        self.origin_url = origin_url
        self.username_value = username_value
        self.password_value = password_value
        self.signon_realm = signon_realm
        self.date_created = date_created
        self.date_last_used = date_last_used
        self.date_password_modified = date_password_modified

    def to_dict(self):
        date_created = format_date(self.date_created)
        date_last_used = format_date(self.date_last_used)
        date_password_modified = format_date(self.date_password_modified)
        return {
            'origin_url': self.origin_url,
            'username_value': self.username_value,
            'password_value': self.password_value,
            'signon_realm': self.signon_realm,
            'date_created': date_created,
            'date_last_used': date_last_used,
            'date_password_modified': date_password_modified,
        }
