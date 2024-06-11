# Lumus

Lumus es una utilidad de línea de comandos escrita en Python que proporciona funcionalidades para explorar redes y dominios.

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/emi9310/Lumus.git
cd Lumus
```

2. Instala las dependencias necesarias. Asegúrate de tener Python 3.x instalado en tu sistema.

```bash
pip install -r requirements.txt
```

3. Si aún no tienes instalados `nmap` y `sublist3r`, puedes instalarlos ejecutando los siguientes comandos:

```bash
sudo apt-get update
sudo apt-get install -y nmap sublist3r
```

4. Instala Lumus:

```bash
pip install .
```

## Uso

Una vez instalado, puedes usar Lumus desde la línea de comandos. Aquí hay algunos ejemplos de cómo usarlo:

- Hacer ping a un host:

```bash
lumus host_a_pingear.com
```

- Enumerar subdominios de un dominio:

```bash
lumus dominio.com -e
```

- Escanear vulnerabilidades de un host:

```bash
lumus host_a_escanear.com -v
```

- Obtener ayuda:

```bash
lumus -h
```

## Contribución

Si encuentras algún problema o tienes alguna sugerencia, por favor abre un issue en este repositorio.

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commits (`git commit -am 'Añade nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un nuevo Pull Request.

