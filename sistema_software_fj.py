from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os


# ==============================================================================
# 1. CONFIGURACIÓN DEL ARCHIVO DE LOGS (EVENTOS Y ERRORES)
# ==============================================================================
def configurar_logger(ruta_log: str = "software_fj.log") -> logging.Logger:
    """Crea y configura un logger que escribe eventos y errores en un archivo."""
    logger = logging.getLogger("SoftwareFJLogger")  # Obtiene o crea el logger
    logger.setLevel(logging.INFO)  # Registra desde INFO en adelante (INFO, WARNING, ERROR)

    if not logger.handlers:  # Evita duplicar handlers en ejecuciones repetidas
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        manejador_archivo = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

    return logger



# ==============================================================================
# 1. CONFIGURACIÓN DEL ARCHIVO DE LOGS (EVENTOS Y ERRORES)
# ==============================================================================
def configurar_logger(ruta_log: str = "software_fj.log") -> logging.Logger:
    """Crea y configura un logger que escribe eventos y errores en un archivo."""
    logger = logging.getLogger("SoftwareFJLogger")  # Obtiene o crea el logger
    logger.setLevel(logging.INFO)  # Registra desde INFO en adelante (INFO, WARNING, ERROR)

    if not logger.handlers:  # Evita duplicar handlers en ejecuciones repetidas
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        manejador_archivo = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

    return logger


logger = configurar_logger()


# ==============================================================================
# 2. EXCEPCIONES PERSONALIZADAS DEL DOMINIO
# ==============================================================================
class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados del sistema."""


class ValidacionEntidadError(ErrorSistemaFJ):
    """Se lanza cuando un atributo o parámetro no cumple con las reglas de validación."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta usar o reservar un servicio no disponible."""


class OperacionReservaError(ErrorSistemaFJ):
    """Se lanza cuando ocurre una operación inválida o inconsistente en una reserva."""


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo financiero o de duración resulta inválido."""
# ==============================================================================
# 3. CLASE ABSTRACTA BASE PARA ENTIDADES DEL SISTEMA
# ==============================================================================
class EntidadSistema(ABC):
    """Clase abstracta general para entidades gestionadas en memoria."""

    def __init__(self, id_entidad: str) -> None:
        if not isinstance(id_entidad, str) or not id_entidad.strip():  # Valida ID no vacío
            raise ValidacionEntidadError("El identificador de la entidad debe ser un texto no vacío.")
        self._id_entidad = id_entidad.strip().upper()  # Encapsula el identificador normalizado
        self._fecha_registro = datetime.now()  # Registra fecha y hora de creación

    @property
    def id_entidad(self) -> str:
        """Acceso de solo lectura al identificador de la entidad."""
        return self._id_entidad

    @property
    def fecha_registro(self) -> datetime:
        """Acceso de solo lectura a la fecha de creación."""
        return self._fecha_registro

    @abstractmethod
    def validar(self) -> None:
        """Cada entidad debe implementar su propia validación integral."""

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción legible de la entidad."""


# ==============================================================================
# 4. CLASE CLIENTE (ENCAPSULACIÓN Y VALIDACIONES ESTRICTAS)
# ==============================================================================
class Cliente(EntidadSistema):
    """Representa un cliente con datos personales encapsulados y validados."""

    def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str) -> None:
        super().__init__(id_entidad)  # Inicializa atributos comunes en EntidadSistema
        self.nombre = nombre  # Invoca el setter de nombre para validar
        self.correo = correo  # Invoca el setter de correo para validar
        self.telefono = telefono  # Invoca el setter de teléfono para validar
        self.validar()  # Ejecuta validación completa del objeto

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:  # Exige mínimo 3 caracteres
            raise ValidacionEntidadError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValidacionEntidadError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) < 7:
            raise ValidacionEntidadError("El teléfono debe contener solo dígitos (mínimo 7).")
        self._telefono = valor.strip()

    def validar(self) -> None:
        if not self._nombre or not self._correo or not self._telefono:
            raise ValidacionEntidadError("Faltan datos obligatorios en el perfil del cliente.")

    def describir(self) -> str:
        return (
            f"Cliente [{self._id_entidad}] - Nombre: {self._nombre} | "
            f"Correo: {self._correo} | Tel: {self._telefono}"
        )
