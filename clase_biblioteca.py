import functools
from datetime import datetime

from clases_metaclases import Prestamo


def registrar_operacion(funcion):
    """Decorador propio: anota en la bitacora de la biblioteca cada operacion
    de gestion que se ejecuta, con la hora. Se aplica a los metodos que
    modifican el estado del sistema."""

    @functools.wraps(funcion)
    def envoltura(self, *args, **kwargs):
        resultado = funcion(self, *args, **kwargs)
        marca = datetime.now().strftime("%H:%M:%S")
        self.bitacora.append(f"[{marca}] {funcion.__name__}")
        return resultado

    return envoltura


class Biblioteca:
    """Patron Singleton: solo puede existir una instancia de la biblioteca,
    que actua como punto de acceso unico al catalogo central."""

    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, nombre="", correo=""):
        # Evita reinicializar el estado si se vuelve a "instanciar".
        if getattr(self, "_inicializada", False):
            return
        self.nombre = nombre
        self.correo = correo
        self.libros = []      # agregacion: existen sin la biblioteca
        self.usuarios = []    # agregacion: existen sin la biblioteca
        self.prestamos = []   # composicion: los crea y posee la biblioteca
        self.bitacora = []
        self._inicializada = True
        SELF.observadores = []

    # ---------- helpers privados ----------
    def _buscar_libro(self, isbn):
        return next((l for l in self.libros if l.isbn == isbn), None)

    def _buscar_usuario(self, dni):
        return next((u for u in self.usuarios if u._dni == dni), None)

    def _tiene_prestamo_activo(self, libro):
        return any(p.libro is libro and p.esta_activo() for p in self.prestamos)

    # ---------- gestion de libros ----------
    @registrar_operacion
    def agregar_libro(self, libro):
        if self._buscar_libro(libro.isbn):
            raise ValueError(f"Ya existe un libro con ISBN {libro.isbn}")
        self.libros.append(libro)

    @registrar_operacion
    def baja_libro(self, isbn):
        libro = self._buscar_libro(isbn)
        if libro is None:
            raise ValueError("Libro inexistente")
        self.libros.remove(libro)

    @registrar_operacion
    def modificar_libro(self, isbn, **campos):
        libro = self._buscar_libro(isbn)
        if libro is None:
            raise ValueError("Libro inexistente")
        for clave, valor in campos.items():
            setattr(libro, clave, valor)

    def listar_libros(self):
        return [l.obtener_info() for l in self.libros]

    # ---------- gestion de usuarios ----------
    @registrar_operacion
    def agregar_usuario(self, usuario):
        if self._buscar_usuario(usuario._dni):
            raise ValueError(f"Ya existe un usuario con DNI {usuario._dni}")
        self.usuarios.append(usuario)

    @registrar_operacion
    def baja_usuario(self, dni):
        usuario = self._buscar_usuario(dni)
        if usuario is None:
            raise ValueError("Usuario inexistente")
        self.usuarios.remove(usuario)

    @registrar_operacion
    def modificar_usuario(self, dni, **campos):
        usuario = self._buscar_usuario(dni)
        if usuario is None:
            raise ValueError("Usuario inexistente")
        for clave, valor in campos.items():
            setattr(usuario, f"_{clave}", valor)

    def listar_usuarios(self):
        return [u.obtener_info() for u in self.usuarios]

    # ---------- gestion de prestamos ----------
    @registrar_operacion
    def registrar_prestamo(self, isbn, dni):
        libro = self._buscar_libro(isbn)
        usuario = self._buscar_usuario(dni)
        if libro is None or usuario is None:
            raise ValueError("Libro o usuario inexistente")
        if self._tiene_prestamo_activo(libro):
            raise ValueError(f"El libro '{libro.titulo}' ya tiene un prestamo activo")
        prestamo = Prestamo(libro, usuario)  # composicion: lo crea la biblioteca
        self.prestamos.append(prestamo)
        usuario.historial_de_prestamo.append(prestamo)
        return prestamo

    @registrar_operacion
    def registrar_devolucion(self, isbn):
        for p in self.prestamos:
            if p.libro.isbn == isbn and p.esta_activo():
                p.registrar_devolucion()
                return p
        raise ValueError("No hay un prestamo activo para ese libro")

    def prestamos_activos(self):
        return [p for p in self.prestamos if p.esta_activo()]
