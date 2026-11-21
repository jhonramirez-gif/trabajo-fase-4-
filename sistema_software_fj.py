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
