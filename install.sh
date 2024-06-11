#!/bin/bash

# Renombrar el archivo
mv lumus.py lumus

# Agregar el shebang
echo '#!/usr/bin/env python3' | cat - lumus > temp && mv temp lumus

# Dar permisos de ejecución
chmod +x lumus

# Mover el archivo a /usr/local/bin
sudo mv lumus /usr/local/bin
