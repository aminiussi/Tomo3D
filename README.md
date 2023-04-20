# TOMO3D_dev
Download the zip file. It contains the source files and different folders.

To compile this new version, dentro de la carpeta build/:
  1. Modificar el archivo install_new.sh. Hay dos paths que tenéis que modificar, según donde pongáis este código y según dónde tengáis la librería "boost", necesaria para el funcionamiento del tomo3d.
  2. Ejecutar este archivo en terminal (bash install_new.sh).
  3. Compilar en terminal con make.
  4. El nuevo ejecutable tt_inverse3d aparecerá en esta carpeta build/. Simplemente acordaros de cambiar en vuestro .bashrc, el path al ejecutable al de esta nueva versión.
