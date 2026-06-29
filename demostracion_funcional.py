from datetime import timedelta

from clases_metaclases import Usuario, Administrador, Libro, MetaEntidad
from clase_biblioteca import Biblioteca

def mostrar_info(elementos):
    """Polimorfismo: recorre objetos distintos y todos responden obtener_info()."""
    for e in elementos:
        print(" -", e.obtener_info())


def main():
    biblio = Biblioteca("Biblioteca UNaB", "biblio@unab.edu.ar")

    # Confirmamos que Singleton funciona: otra "instancia" es la misma.
    otra = Biblioteca()
    print("Es la misma instancia?", biblio is otra)

    # Damos de alta un administrador y un par de usuarios
    admin = Administrador("Diego", "Luparello", "30111222", "diego@unab.edu.ar", nivel_acceso=3)
    ana = Usuario("Ana", "Gomez", "40222333", "ana@mail.com")
    luis = Usuario("Luis", "Perez", "41333444", "luis@mail.com")
    admin.gestionar_usuario(biblio, ana)
    admin.gestionar_usuario(biblio, luis)

    # Alta de libros (el administrador gestiona)
    libro1 = Libro("Fluent Python", "Luciano Ramalho", "978-1", 2015, 790)
    libro2 = Libro("Clean Code", "Robert C. Martin", "978-2", 2008, 464)
    admin.gestionar_libro(biblio, libro1)
    admin.gestionar_libro(biblio, libro2)

    print("\nCatalogo de libros:")
    mostrar_info(biblio.libros)

    print("\nPersonas registradas (polimorfismo sobre la jerarquia):")
    mostrar_info([admin, ana, luis])

    # Prestamos
    print("\n--- Prestamos ---")
    admin.gestionar_prestamo(biblio, "978-1", "40222333")
    print("Ana se llevo Fluent Python")

    # Intentar prestar un libro ya prestado debe fallar
    try:
        biblio.registrar_prestamo("978-1", "41333444")
    except ValueError as e:
        print("Error esperado:", e)

    print("Prestamos activos:", len(biblio.prestamos_activos()))

    # Devolucion y nuevo prestamo del mismo libro
    biblio.registrar_devolucion("978-1")
    print("Ana devolvio el libro. Activos ahora:", len(biblio.prestamos_activos()))
    biblio.registrar_prestamo("978-1", "41333444")
    print("Ahora lo tiene Luis. Activos:", len(biblio.prestamos_activos()))

    # Modificacion y baja
    biblio.modificar_libro("978-2", anio=2009)
    biblio.baja_usuario("40222333")
    print("\nUsuarios tras la baja de Ana:")
    mostrar_info(biblio.usuarios)

    # Metaclase: entidades registradas automaticamente
    print("\nEntidades registradas por la metaclase:", MetaEntidad.entidades())

    # Decorador: bitacora de operaciones
    print("\nBitacora de operaciones (decorador):")
    for linea in biblio.bitacora:
        print(" ", linea)

    # Patron Observer: Luis se entera si se vencio el plazo de su prestamo
    print("\n--- Patron Observer (aviso de vencimiento) ---")
    biblio.agregar_observador(luis)
    prestamo_luis = biblio.prestamos_activos()[0]
    prestamo_luis.fecha_prestamo -= timedelta(days=10)  # simulamos que se vencio
    biblio.plazo_entrega(prestamo_luis)


if __name__ == "__main__":
    main()
