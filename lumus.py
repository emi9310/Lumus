#!/usr/bin/env python3
import argparse
import subprocess
from colorama import Fore, Style


def hacer_ping(host):
    resultado = subprocess.run(['ping', host], capture_output=True, text=True)
    lineas = resultado.stdout.split('\n')
    ip = ""
    sistema_operativo = ""
    
    for linea in lineas:
        if "Respuesta desde" in linea:
            ip = linea.split()[2][:-1]
            break
    
    print(Fore.MAGENTA + f"\nIP: {ip}\n" + Style.RESET_ALL)
    
    if "Host de destino inaccesible\n" in resultado.stdout:
        print(Fore.RED + "El host está fuera de línea" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "ONLINE" + Style.RESET_ALL)
    
    for linea in lineas:
        if "Tiempo=" in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
        elif "TTL=" in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
        elif "perdidos" in linea:
            print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
            break
    
    if "ttl=" in resultado.stdout.lower():
        sistema_operativo = "Linux"
    elif "ttl=" in resultado.stdout:
        sistema_operativo = "Windows"
    else:
        sistema_operativo = "No se pudo determinar el sistema operativo"
    
    print(Fore.BLUE + f"Sistema operativo: {sistema_operativo}" + Style.RESET_ALL)

def enumerar_subdominios(dominio):
    print("\n")
    try:
        resultado = subprocess.run(['sublist3r', '-d', dominio], capture_output=True, text=True)
        lineas = resultado.stdout.split('\n')
        for linea in lineas:
            if "Total Unique Subdomains Found" in linea:
                print(Fore.YELLOW + linea + Style.RESET_ALL)
                break
        for linea in lineas:
            if dominio in linea and "." in linea:
                print(Fore.LIGHTBLACK_EX + linea.strip() + Style.RESET_ALL)
    except Exception as e:
        print("Error:", e)

def escanear_vulnerabilidades(host):
    print(Fore.YELLOW + "\nEscaneando vulnerabilidades en", host + Style.RESET_ALL)
    resultado = subprocess.run(['nmap', '-sC', '-sV', '-script', 'vuln', host], capture_output=True, text=True)
    
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
     ██▓     █    ██  ███▄ ▄███▓ █    ██   ██████ 
    ▓██▒     ██  ▓██▒▓██▒▀█▀ ██▒ ██  ▓██▒▒██    ▒ 
    ▒██░    ▓██  ▒██░▓██    ▓██░▓██  ▒██░░ ▓██▄   
    ▒██░    ▓▓█  ░██░▒██    ▒██ ▓▓█  ░██░  ▒   ██▒
    ░██████▒▒▒█████▓ ▒██▒   ░██▒▒▒█████▓ ▒██████▒▒
    ░ ▒░▓  ░░▒▓▒ ▒ ▒ ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
    ░ ░ ▒  ░░░▒░ ░ ░ ░  ░      ░░░▒░ ░ ░ ░ ░▒  ░ ░
      ░ ░    ░░░ ░ ░ ░      ░    ░░░ ░ ░ ░  ░  ░  
        ░  ░   ░            ░      ░           ░  
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
