from flask import Flask, jsonify, request
from flask import render_template
from controllers.cookie_controller import CookieController_Firefox, CookieController_Edge
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
controller_firefox = CookieController_Firefox()
controller_edge = CookieController_Edge()


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


@app.route('/obtener/llave', methods=['GET'])
def obtener_llave_session():
    return jsonify(controller_edge.obtener_llave_session())

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
