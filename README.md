# hypercube

Es un script muy simple escrito en python que hace uso de las bibliotecas 
numpy y matplotlib par proyectar y visualizar un cubo 4D en 3 dimensiones.
Inspirado en el muy buen video del canal Mathologer. [Link](https://youtu.be/E2l95ttmJOg)

## uso
simplemente ejecutar `python main.py`

## Teoría
La idea de proyectar un cubo de N-dimensiones a (N-1)-dimensiones es 
imaginar una luz encima del cubo que emite rayos de luz que luego crean una 
sombra en un plano debajo del cubo, donde este plano es de (N-1)-dimensiones.

Matematicamente esto consta de calcular la recta que une a la luz con cada 
vértice del cubo para luego determinar la intersección del plano con esa recta.

En base a la [clase en UC Davis sobre raytracing](https://youtu.be/Ahp6LDQnK4Y), 
podemos optimizar esta cuenta teniendo en cuenta que la diferencia entre un vértice 
y la luz forman un vector director de esa recta. Luego, pensando en el punto Q que es 
la intersección de la recta con el plano, sabemos que Q es perpendicular a la normal 
del plano (por ser un punto del plano) y por lo tanto el producto interno entre Q y 
la normal del plano es 0. Además, Q es un múltiplo del vector que dirige a la recta 
y por lo tanto es un múltiplo de `(vertice - luz)`. En otras palabras, 
`Q = t*(vertice - luz)` donde `t` es un número real. De aquí solo queda despejar 
`t` para obtener a Q, que es un simple cociente entre dos productos internos.

## Mejoras a futuro
* Hacer posible crear cubos de N-dimensiones y proyectarlos a 3D con llamadas recursivas.
* Implementar la versión 4D como un shader de OpenGL.
* Tener una interfaz de comandos para permitir elegir las dimensiones, si se guarda un 
  video, y cosas similares.