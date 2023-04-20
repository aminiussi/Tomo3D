# TOMO3D_dev

El archivo comprimido contiene las diferentes subrutinas que conforman el tomo3d y distintas carpetas. Esta versión está actualizada con la posibilidad de poder correr datos 2D directamente con los datos de input y scripts originalmente preparados para tomo2D.

Para compilar esta versión, dentro de la carpeta build/:
  1. Modificar el archivo install_new.sh. Hay dos paths que tenéis que modificar, según donde pongáis este código y según dónde tengáis la librería "boost", necesaria para el funcionamiento del tomo3d.
  2. Ejecutar este archivo en terminal (bash install_new.sh).
  3. Compilar en terminal con make.
  4. El nuevo ejecutable tt_inverse3d aparecerá en esta carpeta build/. Simplemente acordaros de cambiar en vuestro .bashrc, el path al ejecutable al de esta nueva versión.
  5. Para correr datos 2D, añadir el flag -2 a la linea de ejecución en el script. No es necesario cambiar nada más en el script preparado originalmente para el tomo2D, ni tampoco modificar los datos de input 2D (solamente cambiar el ejecutable a tt_inverse3d y añadir el flag "-2").
