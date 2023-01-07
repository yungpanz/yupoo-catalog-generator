import os
from setuptools import setup
from distutils.command.build_py import build_py as _build_py
    
class build_exe(_build_py):
    def run(self):
        # Get the name parameter from the setup function
        name = self.distribution.metadata.name

        # Build the pyinstaller command
        command = f'pyinstaller src/main.py --noconfirm --onefile -n {name} --noconsole --paths=src --icon=icons/logo.icns --icon=icons/logo.ico'

        # Execute the command
        os.system(command)

setup(
    name='Yupo-Catalog-Generator',
    version='1.0',
    description='Yupoo products catalog generator',
    author='Paolo Anzani',
    author_email='anzanipaolodev@gmail.com',
    install_requires=['pyqt5', 'reportlab', 'bs4', 'requests'],
    cmdclass={'build_exe': build_exe},
)