#!/usr/bin/env python3

import argparse
import subprocess
import shutil
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────── UTILIDADES DE COLOR Y MENSAJES ───────────────

def imprimir_error(mensaje, stderr=""):
    print(Fore.RED + "[ERROR] " + mensaje + Style.RESET_ALL)
    if stderr:
        print(Fore.RED + stderr.strip() + Style.RESET_ALL)

def imprimir_info(mensaje):
    print(Fore.CYAN + "[INFO] " + mensaje + Style.RESET_ALL)

def imprimir_ok(mensaje):
    print(Fore.GREEN + "[OK] " + mensaje + Style.RESET_ALL)

def imprimir_advertencia(mensaje):
    print(Fore.YELLOW + "[!] " + mensaje + Style.RESET_ALL)

# ─────────────── DEPENDENCIAS ───────────────

def verificar_dependencias(comandos):
    for comando in comandos:
        if not shutil.which(comando):
            imprimir_error(f"'{comando}' no está instalado. Instálalo para continuar.")
            sys.exit(1)

# ─────────────── EJECUCIÓN DE COMANDOS ───────────────

def ejecutar_comando(cmd, descripcion, debug=False):
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode != 0:
            imprimir_error(f"Falló {descripcion}", resultado.stderr)
            return None
        if debug:
            print(Fore.LIGHTBLACK_EX + resultado.stdout + Style.RESET_ALL)
        return resultado.stdout
    except Exception as e:
        imprimir_error(f"Excepción ejecutando {descripcion}: {e}")
        return None

# ─────────────── FUNCIONES PRINCIPALES ───────────────

def hacer_ping(host, debug=False):
    imprimir_info(f"Haciendo ping a {host}")
    salida = ejecutar_comando(['ping', '-c', '4', host], 'ping', debug)
    if not salida:
        return

    lineas = salida.splitlines()
    ip = ""
    for linea in lineas:
        if "PING" in linea:
            ip = linea.split()[2].strip("()")
            break
    print(Fore.MAGENTA + f"\nIP: {ip}" + Style.RESET_ALL)

    if "Destination Host Unreachable" in salida:
        imprimir_error("El host está fuera de línea.")
    else:
        imprimir_ok("ONLINE")

    for linea in lineas:
        if any(x in linea for x in ["time=", "ttl=", "packets transmitted"]):
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)

    sistema_operativo = detectar_sistema_operativo(salida)
    print(Fore.BLUE + f"Sistema operativo: {sistema_operativo}" + Style.RESET_ALL)

def detectar_sistema_operativo(salida):
    if "ttl=" in salida.lower():
        return "Linux"
    elif "TTL=" in salida:
        return "Windows"
    return "Desconocido"

def enumerar_subdominios(dominio, debug=False):
    imprimir_info(f"Enumerando subdominios para {dominio}")
    salida = ejecutar_comando(['sublist3r', '-d', dominio], 'sublist3r', debug)
    if not salida:
        return

    for linea in salida.splitlines():
        if "Total Unique Subdomains Found" in linea:
            print(Fore.YELLOW + linea + Style.RESET_ALL)
        elif dominio in linea and "." in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)

def escanear_vulnerabilidades(host, debug=False):
    imprimir_info(f"Escaneando vulnerabilidades en {host} con Nmap")
    salida = ejecutar_comando(['nmap', '-sC', '-sV', '--script', 'vuln', host], 'nmap', debug)
    if not salida:
        return

    lineas = salida.splitlines()
    rdns_record = ""
    ports_info = []

    for linea in lineas:
        if "rDNS record" in linea:
            rdns_record = linea
        elif "/tcp" in linea:
            ports_info.append(linea.strip())

    if rdns_record:
        print(Fore.LIGHTBLACK_EX + rdns_record + Style.RESET_ALL)

    print(Fore.YELLOW + "\nPORT  STATE  SERVICE VERSION" + Style.RESET_ALL)
    for port in ports_info:
        print(port)

# ─────────────── PROGRAMA PRINCIPAL ───────────────

def main():
    parser = argparse.ArgumentParser(description='Lumus: Herramienta de red todo-en-uno')
    parser.add_argument('host', type=str, help='IP o dominio a explorar')
    parser.add_argument('-e', '--enumerar', action='store_true', help='Enumerar subdominios')
    parser.add_argument('-v', '--vulnerabilidades', action='store_true', help='Escanear vulnerabilidades')
    parser.add_argument('-d', '--debug', action='store_true', help='Mostrar salida completa de comandos')

    args = parser.parse_args()

    print(Fore.GREEN + """
██╗     ██╗   ██╗███╗   ███╗██╗   ██╗███████╗
██║     ██║   ██║████╗ ████║██║   ██║██╔════╝
██║     ██║   ██║██╔████╔██║██║   ██║███████╗
██║     ██║   ██║██║╚██╔╝██║██║   ██║╚════██║
███████╗╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║
╚══════╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝
    """ + Style.RESET_ALL)

    verificar_dependencias(['ping', 'nmap', 'sublist3r'])

    start_time = time.time()

    hacer_ping(args.host, args.debug)

    if args.enumerar:
        enumerar_subdominios(args.host, args.debug)

    if args.vulnerabilidades:
        escanear_vulnerabilidades(args.host, args.debug)

    if not (args.enumerar or args.vulnerabilidades):
        imprimir_advertencia("No se especificó ninguna acción. Usa -h para ver las opciones.")

    duracion = time.time() - start_time
    print(Fore.LIGHTBLACK_EX + f"\nDuración total: {duracion:.2f} segundos" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
