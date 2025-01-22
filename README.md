- Constanstes en MAYÚSCULA (TEMP_ALTA).
- Variables, métodos y funciones en minúscula y en camelCase (tempCielo).
- Clases y estructuras comienzan en mayúscula (Cards).
- Parámetro resolution = 1 si queremos emplear las cartas en tamaño original o
.5 si queremos reducir el tamaño a la mitad.

ETAPAS DEL PROYECTO
1. PREPROCESO
   Eliminar el ruido de las imágenes, eliminar todos los elementos que no son ni palos ni
   figuras del poker.
   Cambiar el tamaño de las cartas (resolution = 1 o resolution = 0.5)
2. SEGMENTADO
   Umbralizar las cartas
   Etiquetar los objetos con colores (label2rgb)
   Crear una clase Cards con los siguientes atributos:
      - imagen color de la carta
      - imagen en gris de la carta
      - centroido
      - BoundingBox
      - algún atributo más
