#!/bin/bash

# Instalar dependencias
echo "Instalando dependencias..."
sudo apt-get update  # Actualizar la lista de paquetes
sudo apt-get install -y python3-pip  # Instalar pip para Python 3
pip3 install colorama  # Instalar la dependencia colorama

# Agregar permisos de ejecución
echo "Agregando permisos de ejecución..."
chmod +x nombre_del_script.py

# Agregar al PATH (opcional)
# Si quieres agregar el script al PATH para ejecutarlo desde cualquier ubicación, descomenta las siguientes líneas:
# echo "Moviendo el script a /usr/local/bin..."
# sudo mv nombre_del_script.py /usr/local/bin/

echo "¡Instalación completada!"
