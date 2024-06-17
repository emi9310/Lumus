#!/bin/bash

# Obtener el directorio actual del script
LUMUS_DIR=$(dirname "$(readlink -f "$0")")

# Función para instalar dependencias
install_dependencies() {
    echo "Instalando dependencias..."
    sudo apt update
    sudo apt install -y python3-pip dos2unix
    pip3 install -r "$LUMUS_DIR/requirements.txt"
}

# Función para convertir archivos a formato Unix
convert_to_unix() {
    echo "Convirtiendo archivos a formato Unix..."
    dos2unix "$LUMUS_DIR/lumus.py"
}

# Función para hacer el script ejecutable y moverlo a /usr/local/bin
install_script() {
    echo "Configurando el script..."
    chmod +x "$LUMUS_DIR/lumus.py"
    sudo cp "$LUMUS_DIR/lumus.py" /usr/local/bin/lumus
    sudo chmod +x /usr/local/bin/lumus
}

# Función para agregar /usr/local/bin al PATH si no está presente
update_path() {
    if ! echo "$PATH" | grep -q "/usr/local/bin"; then
        echo "Actualizando PATH..."
        echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
        source ~/.bashrc
    fi
}

# Función principal para ejecutar todas las tareas de instalación
main() {
    echo "Iniciando instalación de Lumus desde $LUMUS_DIR..."

    # Instalar dependencias
    install_dependencies

    # Convertir archivos a formato Unix
    convert_to_unix

    # Configurar el script y agregar al PATH
    install_script
    update_path

    echo "Lumus se ha instalado correctamente."
    echo "Ahora puedes ejecutar 'lumus <hostname> -e' para usar Lumus."
}

# Ejecutar la función principal
main





# !/bin/bash

# Instalar dependencias
#echo "Instalando dependencias..."
#sudo apt-get update  # Actualizar la lista de paquetes
#sudo apt-get install -y python3-pip  # Instalar pip para Python 3
#pip3 install colorama  # Instalar la dependencia colorama

# Agregar permisos de ejecución
#echo "Agregando permisos de ejecución..."
#chmod +x lumus.py

# Agregar al PATH (opcional)
# Si quieres agregar el script al PATH para ejecutarlo desde cualquier ubicación, descomenta las siguientes líneas:
# echo "Moviendo el script a /usr/local/bin..."
# sudo mv lumus.py /usr/local/bin/

#echo "¡Instalación completada!"
