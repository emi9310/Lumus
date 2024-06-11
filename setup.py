from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

# Clase para personalizar el comando de instalación
class CustomInstall(install):
    def run(self):
        # Llama al método run de la clase padre (install)
        install.run(self)
        
        # Instala nmap y sublist3r usando apt-get
        subprocess.run(['apt-get', 'install', '-y', 'nmap', 'sublist3r'])

setup(
    name='lumus',
    version='0.1',
    packages=find_packages(),
    cmdclass={'install': CustomInstall},  # Usa la clase CustomInstall en lugar de install
    entry_points={
        'console_scripts': [
            'lumus=lumus:main',
        ],
    },
)
