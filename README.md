# Sistema de Gestión de Biblioteca Digital

Trabajo Práctico Final – Unidad I – Programación Avanzada (189)
Universidad Nacional Guillermo Brown – Licenciatura en Ciencia de Datos

## Descripción

Aplicación en Python que permite administrar una biblioteca: alta, baja,
modificación y listado de libros y usuarios, y registro de préstamos y
devoluciones. Un libro no puede prestarse si ya tiene un préstamo activo.
Todo el sistema está modelado con Programación Orientada a Objetos siguiendo
el diagrama UML incluido en el repositorio.

## Integrantes

* Edgar Mendieta
* Sabrina
* Val
* Brenda

## Estructura del proyecto

* `clases_metaclses.py`: metaclase y clases del dominio (Persona, Usuario, Administrador, Libro, Préstamo).
* `clase_biblioteca.py`: clase Biblioteca (Singleton) y el decorador propio.
* `pdf`: diagrama UML del sistema.

## Cómo se cumplen los requerimientos técnicos

* **Herencia:** `Persona` es la clase base; `Usuario` y `Administrador` heredan de ella.
* **Polimorfismo:** todas las personas (y los libros) implementan `obtener_info()` a su manera.
* **Agregación:** `Biblioteca` contiene listas de `Libro` y `Usuario`, que se crean por fuera y existen sin la biblioteca (rombo blanco en el UML).
* **Composición:** los `Prestamo` los crea la propia `Biblioteca` dentro de `registrar_prestamo()`; no existen fuera de ella (rombo negro en el UML).
* **Decorador propio:** `registrar_operacion` envuelve los métodos de gestión y anota cada operación en la bitácora de la biblioteca.
* **Metaclase:** `MetaEntidad` (derivada de `ABCMeta`, que deriva de `type`) registra automáticamente cada clase en un catálogo interno.
* **Patrón de diseño:** Singleton en `Biblioteca`.

## Justificación del patrón de diseño (Singleton)

Se usó **Singleton** en la clase `Biblioteca` porque en el sistema existe una
única biblioteca: un único catálogo de libros, usuarios y préstamos
compartido por todo el programa. El patrón garantiza que, sin importar desde
dónde se la "instancie", siempre se trabaja sobre el mismo estado, evitando
catálogos duplicados o inconsistentes.

Somos conscientes de sus contras (introduce estado global y dificulta el
testing aislado), por eso el acceso al estado queda encapsulado dentro de los
métodos de la clase y no se expone como variable global suelta.
