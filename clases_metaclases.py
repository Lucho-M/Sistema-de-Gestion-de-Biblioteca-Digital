from abc import ABC, ABCMeta, abstractmethod
from datetime import date


class MetaEntidad(ABCMeta):
    """Metaclase del sistema.

    Deriva de ABCMeta (que a su vez deriva de type) para poder convivir con
    las clases abstractas. Su trabajo es llevar un registro automatico de
    todas las clases-entidad: cada vez que se define una clase que la usa,
    queda anotada en el catalogo sin tener que mantener una lista a mano.
    """

    _catalogo = {}

    def __new__(mcs, nombre, bases, atributos):
        cls = super().__new__(mcs, nombre, bases, atributos)
        MetaEntidad._catalogo[nombre] = cls
        return cls

    @classmethod
    def entidades(mcs):
        return sorted(MetaEntidad._catalogo)


class Persona(metaclass=MetaEntidad):
    """Clase base de la jerarquia de herencia. Es abstracta: no se puede
    instanciar directamente porque obtener_info() esta sin implementar."""

    def __init__(self, nombre, apellido, dni, correo):
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self._correo = correo

    @abstractmethod
    def obtener_info(self):
        ...


class Observer(ABC):
    """Interfaz del patron Observer: quien se quiera enterar de un vencimiento
    de prestamo tiene que implementar update()."""

    @abstractmethod
    def update(self, prestamo):
        ...


class Usuario(Persona, Observer):
    _ultimo_id = 0

    def __init__(self, nombre, apellido, dni, correo):
        super().__init__(nombre, apellido, dni, correo)
        Usuario._ultimo_id += 1
        self._id = Usuario._ultimo_id
        self.historial_de_prestamo = []  # list[Prestamo]

    @property
    def id(self):
        return self._id

    # Polimorfismo: cada subclase responde obtener_info() a su manera
    def obtener_info(self):
        return f"Usuario #{self._id}: {self._nombre} {self._apellido} (DNI {self._dni})"

    def update(self, prestamo):
        mensaje = (
            f"Estimado/a {self._nombre},\n\n"
            f"Nos comunicamos para informarle que el plazo de devolución "
            f"del libro '{prestamo.libro.titulo}' ha expirado.\n"
            f"Por favor acérquese a la biblioteca para regularizar su situación.\n\n"
            f"Saludos cordiales,\n"
            f"La Biblioteca."
        )
        print(f"[EMAIL a {self._correo}] Vencimiento de plazo\n{mensaje}\n")


class Administrador(Persona, Observer):
    def __init__(self, nombre, apellido, dni, correo, nivel_acceso=1):
        super().__init__(nombre, apellido, dni, correo)
        self._nivel_acceso = nivel_acceso

    def obtener_info(self):
        return f"Administrador {self._nombre} {self._apellido} (nivel {self._nivel_acceso})"

    # El administrador dispara las operaciones de gestion sobre la biblioteca.
    def gestionar_libro(self, biblioteca, libro):
        biblioteca.agregar_libro(libro)

    def gestionar_usuario(self, biblioteca, usuario):
        biblioteca.agregar_usuario(usuario)

    def gestionar_prestamo(self, biblioteca, isbn, dni):
        return biblioteca.registrar_prestamo(isbn, dni)

    def update(self, prestamo):
        mensaje = (
            f"El préstamo del libro '{prestamo.libro.titulo}'\n"
            f"correspondiente al usuario {prestamo.usuario._nombre}\n"
            f"ha expirado."
        )
        print(f"[EMAIL a {self._correo}] Vencimiento de plazo\n{mensaje}\n")


class Libro(metaclass=MetaEntidad):
    def __init__(self, titulo, autor, isbn, anio, paginas):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio = anio
        self.paginas = paginas

    def obtener_info(self):
        return f"'{self.titulo}' de {self.autor} ({self.anio}) - ISBN {self.isbn}"


class Prestamo(metaclass=MetaEntidad):
    def __init__(self, libro, usuario, dias_plazo):
        self.libro = libro
        self.usuario = usuario
        self.dias_plazo = dias_plazo
        self.fecha_prestamo = date.today()
        self.fecha_devolucion = None
        self.activo = True

    def registrar_devolucion(self):
        self.activo = False
        self.fecha_devolucion = date.today()

    def esta_activo(self):
        return self.activo
