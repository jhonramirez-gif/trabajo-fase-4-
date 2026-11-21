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
# ==============================================================================
# 6. CLASE RESERVA (GESTIÓN DE ESTADO, CONFIRMACIÓN Y CANCELACIÓN)
# ==============================================================================
class Reserva(EntidadSistema):
    """Integra un Cliente, un Servicio, duración y estado con manejo de excepciones."""

    ESTADOS_PERMITIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA"}

    def __init__(
        self,
        id_entidad: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
    ) -> None:
        super().__init__(id_entidad)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_final = 0.0
        self.validar()

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_final(self) -> float:
        return self._costo_final

    def validar(self) -> None:
        if not isinstance(self._cliente, Cliente):
            raise ValidacionEntidadError("La reserva exige un objeto Cliente válido.")
        if not isinstance(self._servicio, Servicio):
            raise ValidacionEntidadError("La reserva exige un objeto Servicio válido.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.id_entidad}' no se encuentra disponible."
            )
        self._servicio.validar_parametros_operacion(self._duracion)

    def procesar_y_confirmar(self, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        """Procesa el costo y confirma la reserva aplicando try/except/else/finally."""
        resultado_final = "SIN_CAMBIOS"
        try:
            self.validar()  # Revalida disponibilidad y duración antes de cobrar
            if self._estado == "CANCELADA":
                raise OperacionReservaError(
                    f"No se puede confirmar la reserva '{self._id_entidad}' porque está CANCELADA."
                )
            if self._estado == "CONFIRMADA":
                raise OperacionReservaError(
                    f"La reserva '{self._id_entidad}' ya fue CONFIRMADA previamente."
                )

            # Calcula costo usando la sobrecarga con parámetros opcionales
            costo = self._servicio.calcular_costo(
                self._duracion,
                descuento_pct=descuento_pct,
                impuesto_pct=impuesto_pct,
            )
        except ErrorSistemaFJ as exc:
            resultado_final = f"ERROR ({type(exc).__name__})"
            logger.error(
                "Fallo al procesar reserva %s: %s",
                self._id_entidad,
                exc,
                exc_info=True,
            )
            raise  # Relanza la excepción para que el gestor la maneje sin detener el programa
        else:
            # Solo se ejecuta si no hubo excepciones en try ni en except
            self._costo_final = costo
            self._estado = "CONFIRMADA"
            resultado_final = "CONFIRMADA"
            logger.info(
                "Reserva %s CONFIRMADA | Cliente: %s | Servicio: %s | Total: $%.2f",
                self._id_entidad,
                self._cliente.id_entidad,
                self._servicio.id_entidad,
                self._costo_final,
            )
            return self._costo_final
        finally:
            # Se ejecuta siempre, haya error o éxito
            logger.info(
                "Cierre de procesamiento para reserva %s -> Estado actual: %s | Resultado: %s",
                self._id_entidad,
                self._estado,
                resultado_final,
            )

    def cancelar(self) -> None:
        """Cancela la reserva si su estado actual lo permite."""
        if self._estado == "CANCELADA":
            raise OperacionReservaError(
                f"La reserva '{self._id_entidad}' ya está en estado CANCELADA."
            )
        self._estado = "CANCELADA"
        logger.info("Reserva %s ha sido CANCELADA.", self._id_entidad)

    def describir(self) -> str:
        return (
            f"Reserva [{self._id_entidad}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.id_entidad} | Servicio: {self._servicio.id_entidad} | "
            f"Duración: {self._duracion} | Costo: ${self._costo_final:.2f}"
        )


# ==============================================================================
# 7. GESTOR EN MEMORIA (SIN BASE DE DATOS)
# ==============================================================================
class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en listas internas y registra eventos."""

    def __init__(self) -> None:
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, id_entidad: str, nombre: str, correo: str, telefono: str) -> Cliente:
        cliente = Cliente(id_entidad, nombre, correo, telefono)
        self.clientes.append(cliente)
        logger.info("Cliente registrado en memoria: %s", cliente.describir())
        return cliente

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        servicio.validar()
        self.servicios.append(servicio)
        logger.info("Servicio registrado en memoria: %s", servicio.describir())
        return servicio

    def crear_reserva(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int) -> Reserva:
        reserva = Reserva(id_reserva, cliente, servicio, duracion)
        self.reservas.append(reserva)
        logger.info("Reserva creada en estado PENDIENTE: %s", reserva.describir())
        return reserva


# ==============================================================================
# 8. SIMULACIÓN SECUENCIAL DE 12 OPERACIONES (VÁLIDAS E INVÁLIDAS)
# ==============================================================================
def ejecutar_simulacion() -> None:
    """Ejecuta al menos 10 operaciones completas verificando resiliencia y logging."""
    gestor = GestorSoftwareFJ()
    print("=== INICIO DE SIMULACIÓN SOFTWARE FJ (SIN BASE DE DATOS) ===\n")

    def ejecutar_paso(numero_paso: int, descripcion_paso: str, accion) -> None:
        """Ejecuta una operación de forma aislada para que los errores no detengan el flujo."""
        print(f"--- Paso {numero_paso}: {descripcion_paso} ---")
        try:
            salida = accion()
            print(f"[OK] {salida}\n")
        except ErrorSistemaFJ as exc:
            # Registra la excepción controlada sin interrumpir la simulación
            msg = f"Error controlado en paso {numero_paso} ({type(exc).__name__}): {exc}"
            logger.error(msg)
            print(f"[ERROR CONTROLADO] {exc}\n")
        except Exception as exc:
            # Encadena cualquier error inesperado dentro de una excepción del sistema
            error_encadenado = OperacionReservaError(
                f"Fallo inesperado en paso {numero_paso}: {exc}"
            )
            logger.error("Error inesperado encadenado: %s", error_encadenado, exc_info=True)
            print(f"[ERROR INESPERADO CONTROLADO] {error_encadenado}\n")

    # Variables compartidas entre pasos secuenciales
    estado_sim = {}

    # 1. Registro válido de cliente 1
    ejecutar_paso(
        1,
        "Registro válido de cliente (Ana Gómez)",
        lambda: estado_sim.setdefault(
            "cliente_1",
            gestor.registrar_cliente("CLI-01", "Ana Gómez", "ana.gomez@correo.com", "3001234567"),
        ).describir(),
    )

    # 2. Registro inválido de cliente (correo sin dominio válido)
    ejecutar_paso(
        2,
        "Registro inválido de cliente (correo mal formado)",
        lambda: gestor.registrar_cliente("CLI-02", "Luis Pérez", "correo_invalido", "3009876543").describir(),
    )

    # 3. Registro válido de cliente 2
    ejecutar_paso(
        3,
        "Registro válido de cliente (Carlos Ruiz)",
        lambda: estado_sim.setdefault(
            "cliente_2",
            gestor.registrar_cliente("CLI-03", "Carlos Ruiz", "carlos.ruiz@empresa.co", "3154448899"),
        ).describir(),
    )

    # 4. Creación válida de servicio ReservaSala
    ejecutar_paso(
        4,
        "Creación válida de servicio ReservaSala",
        lambda: estado_sim.setdefault(
            "sala_1",
            gestor.registrar_servicio(
                ReservaSala("SRV-SALA-1", "Sala Ejecutiva Norte", 50.0, capacidad_personas=12, disponible=True)
            ),
        ).describir(),
    )

    # 5. Creación válida de servicio AlquilerEquipo
    ejecutar_paso(
        5,
        "Creación válida de servicio AlquilerEquipo",
        lambda: estado_sim.setdefault(
            "equipo_1",
            gestor.registrar_servicio(
                AlquilerEquipo("SRV-EQ-1", "Proyector Láser 4K", 35.0, serial_equipo="PRJ-9981", disponible=True)
            ),
        ).describir(),
    )

    # 6. Creación válida de servicio AsesoriaEspecializada
    ejecutar_paso(
        6,
        "Creación válida de servicio AsesoriaEspecializada",
        lambda: estado_sim.setdefault(
            "asesoria_1",
            gestor.registrar_servicio(
                AsesoriaEspecializada("SRV-ADV-1", "Arquitectura Cloud", 120.0, area_especialidad="DevOps", disponible=True)
            ),
        ).describir(),
    )

    # 7. Creación inválida de servicio (tarifa no numérica -> encadena excepción)
    ejecutar_paso(
        7,
        "Creación inválida de servicio (tarifa no numérica)",
        lambda: gestor.registrar_servicio(
            ReservaSala("SRV-SALA-ERR", "Sala Beta", "no_es_numero", capacidad_personas=8)  # type: ignore[arg-type]
        ).describir(),
    )

    # 8. Cálculo de costo sobrecargado (con descuento del 10% e impuesto del 19%)
    def paso_8_calculo():
        sala = estado_sim["sala_1"]
        total = sala.calcular_costo(4, descuento_pct=10.0, impuesto_pct=19.0)
        return f"Costo calculado para 4h en {sala.id_entidad} (10% desc, 19% imp): ${total:.2f}"

    ejecutar_paso(8, "Cálculo sobrecargado de costo con descuento e impuesto", paso_8_calculo)

    # 9. Reserva exitosa y confirmación
    def paso_9_reserva_exitosa():
        res = gestor.crear_reserva("RES-001", estado_sim["cliente_1"], estado_sim["sala_1"], duracion=3)
        estado_sim["reserva_1"] = res
        total = res.procesar_y_confirmar(descuento_pct=5.0, impuesto_pct=19.0)
        return f"{res.describir()} -> Confirmada por ${total:.2f}"

    ejecutar_paso(9, "Reserva exitosa y confirmación de Sala", paso_9_reserva_exitosa)

    # 10. Intento de reserva sobre servicio NO disponible (debe fallar y registrarse en log)
    def paso_10_servicio_no_disponible():
        equipo = estado_sim["equipo_1"]
        equipo.disponible = False  # Marca el equipo como no disponible
        return gestor.crear_reserva("RES-002", estado_sim["cliente_2"], equipo, duracion=2).describir()

    ejecutar_paso(10, "Reserva fallida por servicio no disponible", paso_10_servicio_no_disponible)

    # 11. Operación no permitida: intentar confirmar de nuevo una reserva ya confirmada
    def paso_11_reconfirmar_reserva():
        res = estado_sim["reserva_1"]
        return str(res.procesar_y_confirmar())

    ejecutar_paso(11, "Operación no permitida al reconfirmar reserva ya confirmada", paso_11_reconfirmar_reserva)

    # 12. Cancelación válida de reserva y posterior intento de cancelarla otra vez
    def paso_12_cancelacion_y_duplicado():
        res_nueva = gestor.crear_reserva("RES-003", estado_sim["cliente_2"], estado_sim["asesoria_1"], duracion=2)
        res_nueva.cancelar()
        res_nueva.cancelar()  # Segunda cancelación provoca OperacionReservaError
        return res_nueva.describir()

    ejecutar_paso(12, "Cancelación válida seguida de segunda cancelación inválida", paso_12_cancelacion_y_duplicado)

    print("=== RESUMEN FINAL EN MEMORIA ===")
    print(f"Clientes registrados: {len(gestor.clientes)}")
    print(f"Servicios registrados: {len(gestor.servicios)}")
    print(f"Reservas creadas: {len(gestor.reservas)}")
    print(f"Archivo de log generado en: {os.path.abspath('software_fj.log')}")


if __name__ == "__main__":
    ejecutar_simulacion()
