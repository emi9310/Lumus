#!/usr/bin/env python3

import argparse
import subprocess
from colorama import Fore, Style
import sys
import time

def hacer_ping(host):
    try:
        resultado = subprocess.run(['ping', '-c', '4', host], capture_output=True, text=True)
    except Exception as e:
        print(Fore.RED + f"Error al ejecutar ping: {e}" + Style.RESET_ALL)
        return

    if resultado.returncode != 0:
        print(Fore.RED + "Error en el comando ping. Verifique el host y los permisos." + Style.RESET_ALL)
        print(Fore.RED + resultado.stderr + Style.RESET_ALL)
        return

    lineas = resultado.stdout.split('\n')
    ip = ""
    sistema_operativo = ""

    for linea in lineas:
        if "PING" in linea:
            ip = linea.split()[2].strip('()')
            break

    print(Fore.MAGENTA + f"\nIP: {ip}\n" + Style.RESET_ALL)

    if "Destination Host Unreachable" in resultado.stdout:
        print(Fore.RED + "El host está fuera de línea" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "ONLINE" + Style.RESET_ALL)

    for linea in lineas:
        if "time=" in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
        elif "ttl=" in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
        elif "packets transmitted" in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
            break

    if "ttl=" in resultado.stdout.lower():
        sistema_operativo = "Linux"
    elif "TTL=" in resultado.stdout:
        sistema_operativo = "Windows"
    else:
        sistema_operativo = "No se pudo determinar el sistema operativo"

    print(Fore.BLUE + f"Sistema operativo: {sistema_operativo}" + Style.RESET_ALL)

def enumerar_subdominios(dominio):
    print("\n")
    try:
        resultado = subprocess.run(['sublist3r', '-d', dominio], capture_output=True, text=True)
    except Exception as e:
        print(Fore.RED + f"Error al ejecutar sublist3r: {e}" + Style.RESET_ALL)
        return

    if resultado.returncode != 0:
        print(Fore.RED + "Error en el comando sublist3r. Verifique el dominio y los permisos." + Style.RESET_ALL)
        print(Fore.RED + resultado.stderr + Style.RESET_ALL)
        return

    lineas = resultado.stdout.split('\n')
    for linea in lineas:
        if "Total Unique Subdomains Found" in linea:
            print(Fore.YELLOW + linea + Style.RESET_ALL)
            break
    for linea in lineas:
        if dominio in linea and "." in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)

def escanear_vulnerabilidades(host):
    print(Fore.YELLOW + "\nEscaneando vulnerabilidades en", host + Style.RESET_ALL)
    try:
        resultado = subprocess.run(['nmap', '-sC', '-sV', '--script', 'vuln', host], capture_output=True, text=True)
    except Exception as e:
        print(Fore.RED + f"Error al ejecutar nmap: {e}" + Style.RESET_ALL)
        return

    if resultado.returncode != 0:
        print(Fore.RED + "Error en el comando nmap. Verifique el host y los permisos." + Style.RESET_ALL)
        print(Fore.RED + resultado.stderr + Style.RESET_ALL)
        return

    lineas = resultado.stdout.split('\n')
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
    for port_info in ports_info:
        print(port_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Programa Lumus con banderas.')

    parser.add_argument('host', type=str, help='IP o Dominio a explorar')
    parser.add_argument('-e', '--enumerar', action='store_true', help='Enumerar subdominios del dominio')
    parser.add_argument('-v', '--vulnerabilidades', action='store_true', help='Escanear vulnerabilidades del host')

    args = parser.parse_args()

    nombre = Fore.GREEN + """
▙▄ ▙▟ ▛▚▞▜ ▙▟ ▟▛ 
""" + Style.RESET_ALL

    print(nombre)

    print("Mirando por ahi...")
    hacer_ping(args.host)
    if args.enumerar:
        print("\nSubdominios...")
        enumerar_subdominios(args.host)
    if args.vulnerabilidades:
        escanear_vulnerabilidades(args.host)

    if not (args.enumerar or args.vulnerabilidades):
        print("No se ha especificado ninguna acción. Usa -h para ver las opciones disponibles.")

                                                                                                    

