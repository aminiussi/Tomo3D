# TOMO3D_dev (English)

The compressed file contains the different tomo3d subroutines and different folders. This version is updated with the possibility to run 2D data + script originally prepared for tomo2D.

To compile this version, inside the build/ folder:

1. Modify the install_new.sh file. There are two paths that you have to modify, depending on where you put this code and depending on where you have the "boost" library, necessary for tomo3d to work.
2. Run this file in terminal (bash install_new.sh).
3. Compile in terminal with make.
4. The new tt_inverse3d executable will appear in this build/ folder. Just remember to change in your .bashrc, the path to this executable.
5. To run 2D data, add the -2 flag to the execution line in the script. It is not necessary to change anything else in the script originally prepared for tomo2D, nor to modify the 2D input data (just change the executable to tt_inverse3d and add the "-2" flag). The outputs will also be in 2D format.

# TOMO3D_dev (Spanish)

El archivo comprimido contiene las diferentes subrutinas que conforman el tomo3d y distintas carpetas. Esta versión está actualizada con la posibilidad de poder correr datos 2D directamente con los datos de input y scripts originalmente preparados para tomo2D.

Para compilar esta versión, dentro de la carpeta build/:
  1. Modificar el archivo install_new.sh. Hay dos paths que tenéis que modificar, según donde pongáis este código y según dónde tengáis la librería "boost", necesaria para el funcionamiento del tomo3d.
  2. Ejecutar este archivo en terminal (bash install_new.sh).
  3. Compilar en terminal con make.
  4. El nuevo ejecutable tt_inverse3d aparecerá en esta carpeta build/. Simplemente acordaros de cambiar en vuestro .bashrc, el path  a este ejecutable.
  5. Para correr datos 2D, añadir el flag -2 a la linea de ejecución en el script. No es necesario cambiar nada más en el script preparado originalmente para el tomo2D, ni tampoco modificar los datos de input 2D (solamente cambiar el ejecutable a tt_inverse3d y añadir el flag "-2"). Los outputs también saldrán en formato 2D.
